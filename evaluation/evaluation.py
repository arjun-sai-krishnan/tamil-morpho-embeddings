import pandas as pd

def eval_on_analogy_dset(model, dset, topn, keys=None):
    scores = []
    for idx, rel in dset.items():
        print("Relation id: " + str(idx))
        print("Relation example: " + ' '.join(rel[0]))
        if keys:
            print("Relation name: " + keys[idx])
        length = len(rel)
        num_analogies = 0
        num_correct = 0
        for rect in rel:
            for t in range(4):
                guesses = model.most_similar(positive=[rect[(t+1)%4], rect[(t+3)%4]], negative=[rect[(t+2)%4]], topn=topn)
                num_analogies += 1
                for guess in guesses:
                    if guess[0] == rect[t]:
                        num_correct += 1
                        break
        if num_analogies != 0:
            print("Score out of  " + str(num_analogies) + " analogies: " + str(float(num_correct)/num_analogies))
            scores.append(float(num_correct)/num_analogies)
        else:
            print("No analogies in vocabulary for this relation")
            
    df = pd.DataFrame([scores])
    return df