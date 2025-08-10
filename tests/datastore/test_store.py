from datastore import DataStore


def test_datastore_initialization():
    """DataStore initializes component stores."""
    real_store = DataStore()
    assert real_store.accounts is not None
    assert real_store.players is not None
    assert real_store.global_presets is not None
    assert real_store.account_presets is not None


def test_datastore_isolation():
    """Separate DataStore instances have independent file_store roots."""
    store1 = DataStore()
    store2 = DataStore()
    assert store1 is not store2
    assert store1.file_store is not store2.file_store


def test_seed_no_error(tmp_path):
    """Calling seed on an empty seed path logs error but does not raise."""
    ds = DataStore(data_path=str(tmp_path / "data"), seed_path=str(tmp_path / "missing-seed"))
    ds.seed()  # Should not raise even if seed path missing