import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from vllm import LLM, SamplingParams
from outlines.serve.vllm import JSONLogitsProcessor
from pydantic import BaseModel, conlist

# /home/liyinghao/models/llama-2-7b
model_path = '/home/liyinghao/models/llama-2-7b-chat'

class Output(BaseModel):
    names: conlist(str, max_length=5) # type: ignore
    organizations: conlist(str, max_length=5) # type: ignore
    locations: conlist(str, max_length=5) # type: ignore
    miscellanous: conlist(str, max_length=5) # type: ignore

llm = LLM(
    model=model_path,
    tokenizer=model_path,
    gpu_memory_utilization=0.9,
    max_num_seqs=1,
    enforce_eager=True,
    tensor_parallel_size=1
)

logits_processor = JSONLogitsProcessor(schema=Output, llm=llm.llm_engine, whitespace_pattern='\n')
logits_processor.fsm.vocabulary = list(logits_processor.fsm.vocabulary)

sampling_params = SamplingParams(
    temperature=0, 
    max_tokens=100,
    include_stop_str_in_output=False,
    # prompt_logprobs=1,
    logits_processors=[logits_processor]
)

print('---initial finish---')

query = '''Locate all the names, organizations, locations and other miscellaneous entities in the following sentence: 
"Charles went and saw Anna at the coffee shop Starbucks, which was based in a small town in Germany called Essen.'''

output = llm.generate(query, sampling_params, use_tqdm=False)

print(output)
# for prompt_logprob in output[0].prompt_logprobs:
#     if prompt_logprob:
#         print(prompt_logprob)
# logprobs = [list(prompt_logprob.values())[0].logprob for prompt_logprob in output[0].prompt_logprobs if prompt_logprob]
print(output[0].outputs[0].text)

# for token in output:
#     print(token)