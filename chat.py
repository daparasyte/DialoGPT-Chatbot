from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class Conversation(object):
    chat_history_ids = None
    respond_to = None
    cool_down = 5

    def __init__(self):
        self.chat_history_ids = None
        self.cool_down = 5

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
    
    def generate_response(self, text):
        new_input_ids = self.tokenizer.encode(text + self.tokenizer.eos_token, return_tensors='pt')
        # adding the new user input tokens to the chat history
        bot_input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1) if self.chat_history_ids != None else new_input_ids
        # generating a response while limiting the total chat history to 1000 tokens
        
        # Method 2
        self.chat_history_ids = self.model.generate(
            bot_input_ids,
            do_sample=True, 
            max_length=1000,
            top_k=50, 
            top_p=0.95,
            pad_token_id=self.tokenizer.eos_token_id
        )
        # Model generated text
        generated_text = self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return generated_text
    
    def switch_model(self, model="large"):
        self.tokenizer = AutoTokenizer.from_pretrained(f"microsoft/DialoGPT-{model}")
        self.model = AutoModelForCausalLM.from_pretrained(f"microsoft/DialoGPT-{model}")
        # Deleting history
        self.chat_history_ids = None