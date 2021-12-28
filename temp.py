import os
print(os.listdir('./det/model/template'))

template_dir = './det/model/template'
template = [template_dir+path for path in os.listdir(template_dir)]
print(template)