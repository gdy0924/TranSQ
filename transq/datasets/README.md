## 数据集说明

以iu_xray数据集为例，**目录**如下所示：

iu_xray

​	├─ annotation.json

​	└─ images

​			├─ CXR1000_IM-0003

​					├─  0.png

​					└─  1.png 

​			├─  ......

​			└─ CXR9_IM-2407

​					├─  0.png

​					└─  1.png 

其中，annotation.json文件存储的是由"train"、"val"和"test"三部分组成的字典，每一部分的value都是列表形式，列表中的每一条字典对应一条数据样本。

**数据样例**及字段说明例如下：

```json
{
	"train": [
    	{
        	"id": "CXR2384_IM-0942",	#相应的样本id
        	"report": "The heart size and pulmonary vascularity ...",	#样本对应的医学报告
        	"image_path": ["CXR2384_IM-0942/0.png", "CXR2384_IM-0942/1.png"],	#样本对应图像存储路径
        	"split": "train"	#数据集划分
    	},
    	...
	],
	"val": [
        {
            "id": "CXR2056_IM-0694-1001", 	#相应的样本id
            "report": "The heart size is upper limits of normal. The pulmonary XXXX and mediastinum...",	#样本对应的医学报告
            "image_path": ["CXR2056_IM-0694-1001/0.png", "CXR2056_IM-0694-1001/1.png"],	#样本对应图像存储路径
            "split": "val"	#数据集划分
		},
        ...
    ],
	"test": [
        ...
    ]
}
```

