from station_config_check.titansma import compare_config


def test_compare_config():
    config1 = open('tests/files/config1.ttl', mode='r').read()
    config2 = open('tests/files/config2.ttl', mode='r').read()

    percentage = compare_config.diff_percentage(
        golden_image=config1, running_config=config2)

    assert percentage == 100

    differences = compare_config.diff_list(
        golden_image=config1, running_config=config2)

    assert len(differences) == 0
