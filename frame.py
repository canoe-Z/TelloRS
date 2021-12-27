# 线程4：保存录像功能
def save_video(self):
    while(1):
        # 多线程终止条件
        if gv.get_value("THREAD_STOP"):
                break
        # 保存录像
        if gv.get_value("SAVE"):
            self.ui.lineEdit_tips.setText("正在保存录像...")
            self.video_count += 1
            # 视频的编码格式
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # 视频文件名
            video_name = "video" + str(self.video_count) + ".avi" 
            out = cv2.VideoWriter(video_name, fourcc, self.fps, (int(self.video_width), int(self.video_height)))
            while(1):
                # 多线程终止条件
                if gv.get_value("THREAD_STOP"):
                    break
                # 取当前的实时图像
                img = cv2.cvtColor(self.real_time_img, cv2.COLOR_RGB2BGR)
                out.write(img)
                # 按下停止录像按钮
                if not gv.get_value("SAVE"):
                    out.release()
                    self.ui.lineEdit_tips.setText("已保存第{}段录像".format(self.video_count))
                    break
                sleep(1 / self.fps)
        # 等待一段时间
        sleep(1/100)