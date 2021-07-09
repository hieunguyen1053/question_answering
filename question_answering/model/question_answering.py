import torch
from transformers import XLMRobertaForQuestionAnswering, XLMRobertaTokenizer

tokenizer = XLMRobertaTokenizer.from_pretrained("./question_answering/model/xlm-roberta-large-vi-qa", use_fast=False)
model = XLMRobertaForQuestionAnswering.from_pretrained("./question_answering/model/xlm-roberta-large-vi-qa")

def question_answering(question, text):
    encoding = tokenizer(question, text, return_tensors='pt')
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    start_scores, end_scores = model(input_ids, attention_mask=attention_mask, output_attentions=False)[:2]

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    answer = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
    answer = tokenizer.convert_tokens_to_ids(answer.split())
    answer = tokenizer.decode(answer)
    return answer