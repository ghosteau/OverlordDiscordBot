from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TextClassificationPipeline

def t_prediction(text):
    predictions_hud = pipe(text)
    if predictions_hud[0][0]["label"] == "LABEL_1":
        return True
    else:
        return False

model = AutoModelForSequenceClassification.from_pretrained("OverlordTPresave", num_labels = 2)
tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")
pipe = TextClassificationPipeline(model = model, tokenizer = tokenizer, top_k = None)