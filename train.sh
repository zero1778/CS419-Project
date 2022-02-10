#!/bin/sh
#SBATCH -o /home/pbdang/HCMUS/CS419/CS419-Project/process/misc/model3/slurm_out/%j.out 
python process/misc/model3/train.py data/oxbuild_images_full \
                                    -a 'resnet18' \
                                    --pretrained \
                                    --gpu 0 --batch-size 32 \
                                    --weight process/misc/model3/weight/resnet18

