import glob,cv2,numpy as np
import matplotlib.pyplot as plt
from perception.bases.data_loader_base import DataLoaderBase
from configs.utils.utils import write_hdf5,load_hdf5

class DataLoader(DataLoaderBase):
	def __init__(self, config=None):
		super(DataLoader, self).__init__(config)
		# 路径(data_path)、图片类型(img_type)
		self.train_img_path=config.train_img_path
		self.train_groundtruth_path = config.train_groundtruth_path
		self.train_type=config.train_datatype
		self.val_img_path=config.val_img_path
		self.val_groundtruth_path=config.val_groundtruth_path
		self.val_type = config.val_datatype

		# 实验名称(exp_name)
		self.exp_name=config.exp_name
		self.hdf5_path=config.hdf5_path
		self.height=config.height
		self.width=config.width
		self.num_seg_class=config.seg_num

	##li：导入groundTruth图片
	def _access_dataset(self,origin_path,groundtruth_path,datatype):
		"""
		:param origin_path:  原始图片路径(path for original image)
		:param groundtruth_path:  GT图片路径(path for groundtruth image)
		:param datatype:  图片格式(dataType for origin and gt)
		:return:  张量类型（Tensor） imgs， groundTruth
		"""
		print("orgList=", origin_path)
		print("groundtruth=",groundtruth_path)
		orgList = glob.glob(origin_path+"\\*."+datatype) #文件名列表 filename list
		gtList = glob.glob(groundtruth_path+"\\*."+datatype)
		print("orgList=",orgList, "   gtList=", gtList)
		assert (len(orgList) == len(gtList)) # 原始图片和GT图片数量应当一致

		imgs = np.empty((len(orgList), self.height, self.width, 1))
		groundTruth = np.empty((len(gtList), self.num_seg_class, self.height, self.width))

		##li：匹配gtlist和orglist：
		 #
		for index in range(len(orgList)):
			orgPath=orgList[index]
			orgImg=plt.imread(orgPath)
			print("orgpath=",orgPath)
			imgs[index,:,:,0]=np.asarray(orgImg[:,:,1]*0.75+orgImg[:,:,0]*0.25)

			for no_seg in range(self.num_seg_class):
				gtPath=gtList[index]
				gtImg=plt.imread(gtPath,0)
				gtImg = cv2.cvtColor(gtImg, cv2.COLOR_BGR2GRAY)
				groundTruth[index,no_seg]=np.asarray(gtImg)
		print("[INFO] Reading...")
		##其中np.groundTruth=255.0， 为float32制度
		print("groundTruth=",groundTruth)
		print("int(np.max(groundTruth))=",int(np.max(groundTruth)))
		assert (int(np.max(groundTruth)) == 255)
		assert (np.min(groundTruth) == 0)
		return imgs,groundTruth

	##导入训练集和验证集
	def prepare_dataset(self):

		# 训练图片汇成HDF5合集 preapare train_img/groundtruth.hdf5
		imgs_train, groundTruth=self._access_dataset("C:\\Users\\kk\\Desktop\\Optic-Disc-Unet-master-Braits\\Optic-Disc-Unet-master\\Optic-Disc-Unet-master\\experiments\\OpticDisc\\dataset\\train\\origin","C:\\Users\\kk\\Desktop\\Optic-Disc-Unet-master-Braits\\Optic-Disc-Unet-master\\Optic-Disc-Unet-master\\experiments\\OpticDisc\\dataset\\train\\groundtruth",self.train_type)
		write_hdf5(imgs_train,self.hdf5_path+"/train_img.hdf5")
		write_hdf5(groundTruth, self.hdf5_path+"/train_groundtruth.hdf5")
		print("[INFO] Saving Training Data")
		# 测试图片汇成HDF5合集 preapare val_img/groundtruth.hdf5
		imgs_val, groundTruth = self._access_dataset("C:\\Users\\kk\\Desktop\\Optic-Disc-Unet-master-Braits\\Optic-Disc-Unet-master\\Optic-Disc-Unet-master\\experiments\\OpticDisc\\dataset\\validate\\origin", "C:\\Users\\kk\\Desktop\\Optic-Disc-Unet-master-Braits\\Optic-Disc-Unet-master\\Optic-Disc-Unet-master\\experiments\\OpticDisc\\dataset\\validate\\groundtruth", self.val_type)
		write_hdf5(imgs_val, self.hdf5_path + "/val_img.hdf5")
		write_hdf5(groundTruth, self.hdf5_path + "/val_groundtruth.hdf5")
		print("[INFO] Saving Validation Data")

	def get_train_data(self):
		imgs_train=load_hdf5(self.hdf5_path+"/train_img.hdf5")
		groundTruth=load_hdf5(self.hdf5_path+"/train_groundtruth.hdf5")
		return imgs_train,groundTruth

	def get_val_data(self):
		imgs_val=load_hdf5(self.hdf5_path+"/val_img.hdf5")
		groundTruth=load_hdf5(self.hdf5_path+"/val_groundtruth.hdf5")
		return imgs_val,groundTruth
