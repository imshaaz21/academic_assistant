from core.vector_store import VectorStore

def test_vector_store_initialization():
    """Test that the VectorStore class can initialize and create a collection if it doesn't exist."""
    try:
        vector_store = VectorStore()
        print("VectorStore initialized successfully!")
        print(f"Collection name: {vector_store.collection_name}")
        print(f"Collection exists: {vector_store.collection is not None}")
        return True
    except Exception as e:
        print(f"Error initializing VectorStore: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_vector_store_initialization()
    print(f"Test {'passed' if success else 'failed'}")