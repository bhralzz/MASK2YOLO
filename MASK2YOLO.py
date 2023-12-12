'''



Consider you have folders in structure as below:
    
Dataset:
    train_images: source images collection
    train_labels:
        label1: binary masked file for each source iamge for label1 collection
        label1: binary masked file for each source iamge for label1 collection
        label1: binary masked file for each source iamge for label1 collection
        
        
    valid_images: source images collection
    valid_labels:
        label1: binary masked file for each source iamge for label1 collection
        label1: binary masked file for each source iamge for label1 collection
        label1: binary masked file for each source iamge for label1 collection
        
        
        
############################################        

just set base_path = "D:/Dataset/"
and run the code

two folders will be generated in 

Dataset:
    TR: (train)
        iamges: source images collection
        labels: annotation task collection
        
    VL: (valid)
        iamges: source images collection
        labels: annotation task collection
        
    data.yaml
        ready to use in yolo v8 segmentation
    
    
    
'''

import os
import cv2
import yaml
import shutil
from PIL import Image
from tqdm import tqdm


class YOLOAnnotationExtractor:
    def __init__(self, image_folder, output_folder):
        self.image_folder = image_folder
        self.output_folder = output_folder

    def process_images(self,index):
        # Create the output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)

        for file_name in tqdm(os.listdir(self.image_folder), desc="Processing Images"):
            if file_name.endswith(".png"):
                file_path = os.path.join(self.image_folder, file_name)

                # Read the black and white image
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                h, w = img.shape

                # Extract YOLO segmentation information
                objects_info = []

                contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    # Flatten the contour points
                    points = contour.reshape(-1, 2) / [w, h]

                    # Convert points to YOLO format
                    object_info = f"{index} " + " ".join(map(str, points.flatten()))
                    objects_info.append(object_info)

                # Save YOLO annotation information to text file
                text_file_path = os.path.join(self.output_folder, file_name.replace(".png", ".txt"))
                with open(text_file_path, "a+") as text_file:
                    text_file.write("\n".join(objects_info))


class YOLOAnnotationConverter:
    def __init__(self, base_path):
        self.base_path = base_path
        self.train_path = os.path.join(self.base_path, "TR")
        self.valid_path = os.path.join(self.base_path, "VL")
        
        self.train_images_path = os.path.join(self.base_path, "train_images")
        self.train_labels_path = os.path.join(self.base_path, "train_labels")
        
        self.valid_images_path = os.path.join(self.base_path, "valid_images")
        self.valid_labels_path = os.path.join(self.base_path, "valid_labels")


        self.data_yaml_path = os.path.join(self.base_path, "data.yaml")

    def create_directories(self, path):
        os.makedirs(os.path.join(path, "images"), exist_ok=True)
        os.makedirs(os.path.join(path, "labels"), exist_ok=True)

    def remove_folders_and_yaml(self):
        folders_to_remove = ['TR', 'VL']
        for folder in folders_to_remove:
            folder_path = os.path.join(self.base_path, folder)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

        yaml_file_path = os.path.join(self.base_path, 'data.yml')
        if os.path.exists(yaml_file_path):
            os.remove(yaml_file_path)

    def duplicate_images(self, source_path, dest_path):
        for filename in tqdm(os.listdir(source_path), desc='Copying Images'):
            src_file = os.path.join(source_path, filename)
            dest_file = os.path.join(dest_path, "images", filename)
            shutil.copyfile(src_file, dest_file)
            
    def get_folder_list(self,directory):
        folder_list = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
        return folder_list
    
    def process_labels(self, source_path, dest_path):
        self.class_mapping={}    
        #get folders names
        labels_list=self.get_folder_list(source_path)
        for index,lbl in enumerate(labels_list):
            
            self.class_mapping[index]= lbl
            
            temp_label_path=source_path+'/'+lbl
            extractor = YOLOAnnotationExtractor(temp_label_path, dest_path+'/labels')
            extractor.process_images(index)
            
        self.num_classes = len(self.class_mapping)
        
        return self.class_mapping

    def generate_data_yaml(self,class_mapping):
        class_names='\n'
        # for string in class_mapping:
        #     class_names=class_names+string
        data_yaml = {
            'names': class_mapping,
            'nc': len(class_mapping),
            'test': '',
            'train': os.path.abspath(self.train_path),
            'val': os.path.abspath(self.valid_path)
        }

        with open(self.data_yaml_path, 'w') as yaml_file:
            yaml.dump(data_yaml, yaml_file, default_flow_style=False)
        
        temp=1

def main():
    base_path = "D:/Dataset/"
    converter = YOLOAnnotationConverter(base_path)

    # Step 1: Remove folders and YAML file
    converter.remove_folders_and_yaml()

    # Step 2: Create necessary directories
    converter.create_directories(converter.train_path)
    converter.create_directories(converter.valid_path)

    # Step 3: Duplicate images to the target folders
    converter.duplicate_images(converter.train_images_path, converter.train_path)
    converter.duplicate_images(converter.valid_images_path, converter.valid_path)

    # Step 4: Process labels and generate YOLO format files
    classes_info=converter.process_labels(converter.train_labels_path, converter.train_path)
    converter.process_labels(converter.valid_labels_path, converter.valid_path)

    # Step 5: Generate data.yaml
    converter.generate_data_yaml(classes_info)

if __name__ == "__main__":
    main()
