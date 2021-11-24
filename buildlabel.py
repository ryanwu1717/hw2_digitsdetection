import h5py
from PIL import Image
from torchvision import transforms

def get_name(index, hdf5_data):
    '''get the name from digitStruct'''
    name = hdf5_data['/digitStruct/name']
    return ''.join([chr(v[0]) for v in hdf5_data[name[index][0]]])

def get_bbox(index, hdf5_data):
    '''get the bbox position from digitStruct'''
    attrs = {}
    item = hdf5_data['digitStruct']['bbox'][index].item()
    for key in ['label', 'left', 'top', 'width', 'height']:
        attr = hdf5_data[item][key]
        values = [hdf5_data[attr[i].item()][0][0] for i in range(len(attr))] if len(attr) > 1 else [attr[0][0]]
        attrs[key] = values
    return attrs

f = h5py.File('./dataset/train/digitStruct.mat','r')
for j in range(f['/digitStruct/bbox'].shape[0]):
    IMG_NAME = get_name(j, f)
    row_dict = get_bbox(j, f)
    FILE_NAME = IMG_NAME[:-4]
    image = transforms.ToTensor() (Image.open('./dataset/train/'+IMG_NAME))
    image_size = image.size()
    print (j)
    fp = open("labels/"+FILE_NAME+".txt", "w")
    for i in range(len(row_dict['label'])):
        label_idx = int(row_dict['label'][i])-1
        x_center = (row_dict['left'][i] + row_dict['width'][i]/2)/image_size[2]
        y_center = (row_dict['top'][i] + row_dict['height'][i]/2)/image_size[1]
        width = row_dict['width'][i]/image_size[2]
        height = row_dict['height'][i]/image_size[1]
        fp.write(str(label_idx) + ' ' + str(x_center) + ' ' +
        str(y_center) + ' ' + str(width) + ' '+ str(height) + '\n')
    fp.close()