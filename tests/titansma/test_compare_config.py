from station_config_check.config_check import compare_config


def test_compare_config():
    config1 = open('tests/files/config1.ttl', mode='r').read()
    config2 = open('tests/files/config2.ttl', mode='r').read()

    percentage = compare_config.diff_percentage(
        golden_image=config1, running_config=config2)

    assert percentage == 100

    differences = compare_config.diff_list(
        golden_image=config1, running_config=config2)

    assert len(differences) == 0

    results = compare_config.get_config_check_results(
        hostname='DummyHost',
        golden_image=config1,
        running_config=config2
    )

    assert results['hostname'] == 'DummyHost'
    assert results['state'] == 0
    assert results['output'] == (
        "Similarity between config files: 100.0% | " +
        "'Config'=100.0%;;;;\nChanges:\n")
    config3 = open('tests/files/config3.ttl', mode='r').read()

    results = compare_config.get_config_check_results(
        hostname='DummyHost',
        golden_image=config2,
        running_config=config3
    )

    print(results['output'])

    assert results['state'] == 2
    assert results['output'] == (
        "Similarity between config files: 99.99514364407074% | 'Config'" +
        "=99.99514364407074%;;;;\nChanges:\n <apollo/acquisition/" +
        "storeOnlyLocalData> <http://www.w3.org/1999/02/22-rdf-syntax-ns#" +
        "value> \"false\"^^xsd:boolean.")
