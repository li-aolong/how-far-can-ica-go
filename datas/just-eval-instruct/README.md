---
configs:
- config_name: default
  data_files:
  - split: test
    path: "test_all_with_tags.jsonl"
  # - split: test_regular_only
  #   path: "test_regular.jsonl"
  # - split: test_safety_only
  #   path: "test_red.jsonl"


- config_name: responses
  data_files:
  - split: gpt_4_0613
    path: "responses/gpt-4-0613.json"
  - split: gpt_4_0314
    path: "responses/gpt-4-0314.json"
  - split: gpt_3.5_turbo_0301
    path: "responses/gpt-3.5-turbo-0301.json"
  - split: Mistral_7B_Instruct_v0.1
    path: "responses/Mistral-7B-Instruct-v0.1.json"
  - split: Llama_2_13b_chat_hf
    path: "responses/Llama-2-13b-chat-hf.json"
  - split: Llama_2_70B_chat_GPTQ
    path: "responses/Llama-2-70B-chat-GPTQ.json"
  - split: Llama_2_7b_chat_hf
    path: "responses/Llama-2-7b-chat-hf.json"
  - split: vicuna_13b_v1.5
    path: "responses/vicuna-13b-v1.5.json"
  - split: vicuna_7b_v1.5
    path: "responses/vicuna-7b-v1.5.json"

- config_name: judgements_main
  data_files:
  - split: Mistral_7B_Instruct_v0.1
    path: "judgements/main/Mistral-7B-Instruct-v0.1.json"
  - split: gpt_4_0613
    path: "judgements/main/gpt-4-0613.json"
  - split: gpt_4_0314
    path: "judgements/main/gpt-4-0314.json"
  - split: Llama_2_70B_chat_GPTQ
    path: "judgements/main/Llama-2-70B-chat-GPTQ.json"
  - split: Llama_2_13b_chat_hf
    path: "judgements/main/Llama-2-13b-chat-hf.json"
  - split: vicuna_7b_v1.5
    path: "judgements/main/vicuna-7b-v1.5.json"
  - split: vicuna_13b_v1.5
    path: "judgements/main/vicuna-13b-v1.5.json"
  - split: gpt_3.5_turbo_0301
    path: "judgements/main/gpt-3.5-turbo-0301.json"
  - split: Llama_2_7b_chat_hf
    path: "judgements/main/Llama-2-7b-chat-hf.json"

- config_name: judgements_safety
  data_files:
  - split: Mistral_7B_Instruct_v0.1
    path: "judgements/safety/Mistral-7B-Instruct-v0.1.json"
  - split: gpt_4_0613
    path: "judgements/safety/gpt-4-0613.json"
  - split: gpt_4_0314
    path: "judgements/safety/gpt-4-0314.json"
  - split: Llama_2_70B_chat_GPTQ
    path: "judgements/safety/Llama-2-70B-chat-GPTQ.json"
  - split: Llama_2_13b_chat_hf
    path: "judgements/safety/Llama-2-13b-chat-hf.json"
  - split: vicuna_7b_v1.5
    path: "judgements/safety/vicuna-7b-v1.5.json"
  - split: vicuna_13b_v1.5
    path: "judgements/safety/vicuna-13b-v1.5.json"
  - split: gpt_3.5_turbo_0301
    path: "judgements/safety/gpt-3.5-turbo-0301.json"
  - split: Llama_2_7b_chat_hf
    path: "judgements/safety/Llama-2-7b-chat-hf.json"

---

# Just Eval Instruct

##  Highlights

<div class="col-md-12"> 
      <ul>
          <li><b>Data sources:</b> 
              <a href="https://huggingface.co/datasets/tatsu-lab/alpaca_eval" target="_blank">AlpacaEval</a> (covering 5 datasets), 
              <a href="https://huggingface.co/datasets/GAIR/lima/viewer/plain_text/test" target="_blank">LIMA-test</a>, 
              <a href="https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts" target="_blank">MT-bench</a>, 
              <a href="https://huggingface.co/datasets/Anthropic/hh-rlhf/tree/main/red-team-attempts" target="_blank">Anthropic red-teaming</a>, 
              and <a href="https://github.com/Princeton-SysML/Jailbreak_LLM/blob/main/data/MaliciousInstruct.txt" target="_blank">MaliciousInstruct</a>. </li>
          <li><b>1K examples:</b> 1,000 instructions, including 800 for problem-solving test, and 200 specifically for safety test. </li>
          <li><b>Category:</b> We tag each example with (one or multiple) labels on its task types and topics. </li>  
      </ul>  
</div>


## Distribution

![](http://localhost:3000/images/eval_1.png)