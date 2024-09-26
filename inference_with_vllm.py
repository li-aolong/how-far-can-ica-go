import datasets

eval_set = datasets.load_dataset("/home/liyinghao/papers/how_far_ica_go/datas/alpaca_eval", "alpaca_eval")["eval"]
for example in eval_set:
    # generate here is a placeholder for your models generations
    example["output"] = generate(example["instruction"])