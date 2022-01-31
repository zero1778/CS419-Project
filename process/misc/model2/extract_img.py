import os, cv2
import shutil



gt_path = "./data/gt_files_170407"
img_path = "./data/oxbuild_images"
save_img_path = "./data/oxbuild_images_crop/"

if os.path.isdir(save_img_path) == True:
    shutil.rmtree(save_img_path)
os.mkdir(save_img_path)

def numbering(x):
    if x < 10:
        return '0' + str(x)
    return str(x)
    
idx = 1
for each in sorted(os.listdir(gt_path)):
    if each.endswith('query.txt'):
        with open(gt_path + '/' + each, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split(' ')
                img_name = line[0][5:]
                img_name = img_name + '.jpg'
                print(img_name)
                
                img_dir = img_path + '/' + img_name
                img = cv2.imread(img_dir)
                xmin, ymin, xmax, ymax = int(line[1].split(".")[0]), int(line[2].split(".")[0]), int(line[3].split(".")[0]), int(line[4].split(".")[0])
                img = img[ymin: ymax, xmin: xmax]

                img_name = numbering(idx) + "_" + img_name
                idx += 1
                cv2.imwrite(save_img_path + img_name, img)
            