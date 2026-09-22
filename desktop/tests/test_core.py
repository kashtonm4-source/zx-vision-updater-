import tempfile
from pathlib import Path

from true_vision.drivers.hidhide import HidHideAdapter
from true_vision.drivers.vigem import ViGEmBusAdapter
from true_vision.models import Profile, default_profiles
from true_vision.profiles import ProfileStore

def test_default_profile_count():
    assert len(default_profiles()) == 5

def test_profile_store_persists():
    with tempfile.TemporaryDirectory() as tmp:
        store = ProfileStore(Path(tmp))
        store.profiles[0].shot.release_timing = 8.4
        store.save()
        restored = ProfileStore(Path(tmp))
        assert restored.active().shot.release_timing == 8.4

def test_driver_adapters_do_not_fake_connection():
    assert HidHideAdapter().status().available is False
    assert ViGEmBusAdapter().status().available is False
