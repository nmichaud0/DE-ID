from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import openai

MODEL_ID = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B'

def call_llm(prompt: str):

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID,
                                                 torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                                                 device_map='auto')

    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=10)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))



if __name__ == '__main__':
    call_llm('Hello, who are you ?')
