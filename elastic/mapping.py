from elasticsearch import Elasticsearch


def mapping_http(es):
    mapping = {
        "_doc": {
            "properties": {
                "date": {
                    "type": "date",
                    "format":"yyyy-MM-dd HH:mm:ss||epoch_millis",
                },
                "clientip": {
                    "type": "ip"
                },
                "country": {
                    "type": "text",
                    "fielddata": True,
                },
                "geo_point": {
                    "type": "geo_point",
                },
                "user_agent": {
                    "type": "text",
                },
                "status_code": {
                    "type": "integer",
                },
                "method": {
                    "type": "text"
                },
                "path": {
                    "type": "text",
                    "fielddata": True,
                },
                "parameter": {
                    "type": "text",
                },
            }
        }
    }

    #print(es.indices.get_alias("*"))
    try:
        es.indices.delete(index="http")
    except:
        pass

    es.indices.create(index="http")
    es.indices.put_mapping(index="http", doc_type="_doc", body=mapping, include_type_name=True)


def mapping_ssh(es):
    mapping = {
        "_doc": {
            "properties": {
                "date": {
                    "type": "date",
                    "format":"yyyy-MM-dd HH:mm:ss||epoch_millis",
                },
                "clientip": {
                    "type": "ip"
                },
                "country": {
                    "type": "text",
                    "fielddata": True,
                },
                "geo_point": {
                    "type": "geo_point",
                },
                "username": {
                    "type": "text",
                    "fielddata": True,
                },
                "password": {
                    "type": "text",
                    "fielddata": True,
                },
            }
        }
    }

    #print(es.indices.get_alias("*"))
    try:
        es.indices.delete(index="ssh")
    except:
        pass

    es.indices.create(index="ssh")
    es.indices.put_mapping(index="ssh", doc_type="_doc", body=mapping, include_type_name=True)


def main():
    es = Elasticsearch("localhost:9200")

    mapping_http(es)
    #mapping_ssh(es)


if __name__ == '__main__':
    main()
