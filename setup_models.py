import os
from sentence_transformers import SentenceTransformer

def save_local_model():
    print("Attempting to load sentence-transformers/all-MiniLM-L6-v2 from previous cache...")
    try:
        # This will load it from the default global absolute cache since it succeeded previously
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        target_dir = "./models/all-MiniLM-L6-v2"
        os.makedirs(target_dir, exist_ok=True)
        
        print(f"Saving model physically into {target_dir} ...")
        model.save(target_dir)
        print("Model successfully extracted to local directory!")
    except Exception as e:
        print(f"Failed to copy model: {e}")

if __name__ == "__main__":
    save_local_model()
