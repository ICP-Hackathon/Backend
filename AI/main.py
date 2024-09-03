from db import faiss
from crud import add_text


add_text(['When you fall in love at first sight and decide to go on a date with her, don’t rush. Haste can ruin everything. It’s more important to gradually get to know her and understand her mind. Be patient.'], ['dating_adivce_ai'], ['dating_advice_ai_0'])
print(faiss.db.index_to_docstore_id)
