from models.model import Scenario, simulate

def test_refuses_invalid_recovery_fraction():
    sc = Scenario(
        N0=1000,
        years=1,
        dt_days=1.0,
        o2_storage_days=30,
        water_storage_days=30,
        o2_local_fraction=0.9,
        water_local_fraction=0.9,
        water_recovery_fraction=0.999,  # exceeds verified 0.98
        launch_window_days=780,
        missed_window_probability=0.0,
        import_restore_fraction_o2=0.0,
        import_restore_fraction_water=0.0,
        cruise_days=0,
    )
    try:
        simulate(sc, seed=1)
        assert False, "Expected ValueError"
    except ValueError:
        assert True
