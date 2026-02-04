from transformers import AutoImageProcessor, MobileViTForImageClassification

MODEL_DIR = "model/hf/apple_mobilevit_small"

processor = AutoImageProcessor.from_pretrained(MODEL_DIR)
#feature_extractor = AutoImageProcessor.from_pretrained(MODEL_DIR)
model = MobileViTForImageClassification.from_pretrained(MODEL_DIR)
print("processor.size:", processor.size)
print("model.config.image_size:", model.config.image_size)

model.eval()