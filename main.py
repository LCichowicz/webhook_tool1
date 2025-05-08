from fastapi import FastAPI, Request
import pandas as pd
file_1 = 'data/badania.json'
file_3 = 'data/uczelnie.json'


app = FastAPI()

@app.post('/')
async def tool1(request: Request)-> dict:
    projects_df = pd.read_json(file_1)
    university_df = pd.read_json(file_3)
    data = await request.json()
    input_text = data.get('input', "")
    if input_text.startswith("test"):
        return {'output': input_text}


    df = pd.merge(projects_df, university_df, left_on='uczelnia', right_on='id', suffixes=('_projekt', '_uczelnia') )
    print(df)
    answer = df[df['nazwa_projekt'].str.contains(input_text, case=False)]
    output = []
    if not answer.empty:
        for _, row in answer.iterrows():
            output.append(f"Uczelnia {row['nazwa_uczelnia']} prowadzi projekt {row['nazwa_projekt']}. Sponsor: {row['sponsor']}")
    else:
        output.append('Nie znaleziono informacji zgodnych z zapytaniem')


    while len('\n'.join(output)) > 1024:
        output.pop()
                           

    return {'output': '\n'.join(output)}








    

