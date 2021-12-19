import cv2
import numpy as np
import sys
import glob


class Image_Stitching():
    def __init__(self):
        self.ratio = 0.7
        self.min_match = 10
        self.sift = cv2.SIFT_create()
        self.smoothing_window_size = 200

    def registration_single(self, img1, img2):
        kp1, des1 = self.sift.detectAndCompute(img1, None)
        kp2, des2 = self.sift.detectAndCompute(img2, None)
        matcher = cv2.BFMatcher()
        raw_matches = matcher.knnMatch(des1, des2, k=2)
        good_points = []
        good_matches = []
        for m1, m2 in raw_matches:
            if m1.distance < self.ratio * m2.distance:
                good_points.append((m1.trainIdx, m1.queryIdx))
                good_matches.append([m1])
        img3 = cv2.drawMatchesKnn(
            img1, kp1, img2, kp2, good_matches, None, flags=2)
        cv2.imwrite('./temp/matching.jpg', img3)
        if len(good_points) > self.min_match:
            image1_kp = np.float32(
                [kp1[i].pt for (_, i) in good_points])
            image2_kp = np.float32(
                [kp2[i].pt for (i, _) in good_points])

            index = []
            for i, (kp1, kp2) in enumerate(zip(image1_kp, image2_kp)):
                if abs(kp1[1]-kp2[1]) < 20:
                    index.append(i)

            image1_kp = image1_kp[index]
            image2_kp = image2_kp[index]

            # print(image1_kp.shape)
            # print(image2_kp.shape)

            sum = np.mean(image1_kp-image2_kp, 0)[0]
            # print(np.mean(image1_kp-image2_kp, 0)[0])
            # print(np.std(image1_kp-image2_kp, 0)[0])

            index = []
            for i, (kp1, kp2) in enumerate(zip(image1_kp, image2_kp)):
                if abs(abs(kp1[0]-kp2[0])-sum) < 30:
                    index.append(i)

            image1_kp = image1_kp[index]
            image2_kp = image2_kp[index]

            # for kp1, kp2 in image1_kp, image2_kp:
            H, status = cv2.findHomography(
                image2_kp, image1_kp, cv2.RANSAC, 3.0)
        return H

    def registration(self, imgs):
        # H_list = []
        # for idx, _ in enumerate(imgs[:-1]):
        #     H = self.registration_single(imgs[idx], imgs[idx+1])
        #     H_list.append(H)

        H_list = [self.registration_single(
            imgs[idx], imgs[idx+1]) for idx, _ in enumerate(imgs[:-1])]

        return H_list

    def create_mask(self, img1, img2, version):
        height_img1 = img1.shape[0]
        width_img1 = img1.shape[1]
        width_img2 = img2.shape[1]
        height_panorama = height_img1
        width_panorama = width_img1 + width_img2
        offset = int(self.smoothing_window_size / 2)
        barrier = img1.shape[1] - int(self.smoothing_window_size / 2)
        mask = np.zeros((height_panorama, width_panorama))
        if version == 'left_image':
            mask[:, barrier - offset:barrier +
                 offset] = np.tile(np.linspace(1, 0, 2 * offset).T, (height_panorama, 1))
            mask[:, :barrier - offset] = 1
        else:
            mask[:, barrier - offset:barrier +
                 offset] = np.tile(np.linspace(0, 1, 2 * offset).T, (height_panorama, 1))
            mask[:, barrier + offset:] = 1
        return cv2.merge([mask, mask, mask])

    def blending_single(self, img1, img2, H):
        height_img1 = img1.shape[0]
        width_img1 = img1.shape[1]
        width_img2 = img2.shape[1]
        height_panorama = height_img1
        width_panorama = width_img1 + width_img2

        panorama1 = np.zeros((height_panorama, width_panorama, 3))
        mask1 = self.create_mask(img1, img2, version='left_image')
        panorama1[0:img1.shape[0], 0:img1.shape[1], :] = img1
        panorama1 *= mask1
        mask2 = self.create_mask(img1, img2, version='right_image')
        panorama2 = cv2.warpPerspective(
            img2, H, (width_panorama, height_panorama))*mask2
        result = panorama1+panorama2

        rows, cols = np.where(result[:, :, 0] != 0)
        min_row, max_row = min(rows), max(rows) + 1
        min_col, max_col = min(cols), max(cols) + 1
        final_result = result[min_row:max_row, min_col:max_col, :]
        print(final_result.shape)
        cv2.imwrite('./temp/panorama.jpg', final_result)
        return final_result

    def blending(self, imgs):
        H_list = self.registration(imgs)
        result_list = []
        for i in range(len(imgs)-1):
            if i == 0:
                print(H_list[0])
                print(imgs[0].shape)
                print(imgs[1].shape)
                print('************')
                result = self.blending_single(imgs[0], imgs[1], H_list[0])
                result_list.append(result)
            else:
                print(i)
                H = H_list[0]
                for j in range(0, i):
                    H = np.matmul(H, H_list[j])
                print(H)
                print(result_list[i-1].shape)
                print(imgs[i+1].shape)
                result = self.blending_single(
                    result_list[i-1], imgs[i+1], H)
                #assert(1 == 2)
                result_list.append(result)
        print(len(result_list))


def main():
    # img1 = cv2.imread(argv1)
    # img2 = cv2.imread(argv2)
    import os
    imgs = os.listdir('./data/result/')
    imgs.sort()

    imgs = [os.path.join('./data/result/', img) for img in imgs[13:18]]
    imgs = [cv2.imread(img) for img in imgs]
    # print(imgs)
    # images = glob.glob('./data/result/2M6A1631*.JPG')  # 经人提醒，这里的.jpg应该改为.png
    # print(images)
    # imgs=
    final = Image_Stitching().blending(imgs)
    # cv2.imwrite('./temp/panorama.jpg', final)


if __name__ == '__main__':
    main()
    # try:
    #     main(sys.argv[1], sys.argv[2])
    # except IndexError:
    #     print("Please input two source images: ")
    #     print("For example: python Image_Stitching.py '/Users/linrl3/Desktop/picture/p1.jpg' '/Users/linrl3/Desktop/picture/p2.jpg'")
