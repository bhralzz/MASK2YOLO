# MASK2YOLO
**a source for converting masked binary images collections to yolo v8 format
Consider you have folders in structure as below:
    
Dataset

-train_images: source images collection

-train_labels

--label1: binary masked file for each source iamge for label1 collection

--label2: binary masked file for each source iamge for label2 collection

--label3: binary masked file for each source iamge for label3 collection

-valid_images: source images collection

-valid_labels:

--label1: binary masked file for each source iamge for label1 collection

--label2: binary masked file for each source iamge for label2 collection

--label3: binary masked file for each source iamge for label3 collection

        
        
-valid_images: source images collection

-valid_labels:

--label1: binary masked file for each source iamge for label1 collection

--label2: binary masked file for each source iamge for label2 collection

--label3: binary masked file for each source iamge for label3 collection

Genrated paths in Dataset

-TR: (train)

--iamges: source images collection

--labels: annotation task collection
        
-VL: (valid)

--iamges: source images collection

--labels: annotation task collection
        
data.yaml

    
    
