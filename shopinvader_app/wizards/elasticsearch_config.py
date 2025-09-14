# Copyright 2025 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


ES_DEFAULT_PRODUCT_CONFIG = {
    "settings": {
        "analysis": {
            "char_filter": {"replace": {"type": "mapping", "mappings": ["&=> and "]}},
            "filter": {
                "word_delimiter": {
                    "type": "word_delimiter",
                    "split_on_numerics": False,
                    "split_on_case_change": True,
                    "generate_word_parts": True,
                    "generate_number_parts": True,
                    "catenate_all": True,
                    "preserve_original": True,
                    "catenate_numbers": True,
                }
            },
            "analyzer": {
                "default": {
                    "type": "custom",
                    "char_filter": ["html_strip", "replace"],
                    "tokenizer": "whitespace",
                    "filter": ["lowercase", "word_delimiter"],
                }
            },
            "index": {"sort.field": ["main", "id"], "sort.order": ["desc", "asc"]},
        }
    },
    "mappings": {
        "properties": {
            "hierarchicalCategories": {
                "type": "nested",
                "properties": {
                    "ancestors": {"type": "keyword"},
                    "order": {"type": "integer"},
                    "value": {"type": "keyword"},
                    "level": {"type": "integer"},
                },
            },
            "url_key": {"type": "keyword"},
            "variant_attributes": {
                "properties": {"color": {"type": "text", "fielddata": True}}
            },
            "main": {"type": "boolean"},
            "id": {"type": "integer"},
            "redirect_url_key": {"type": "keyword"},
        }
    },
}

ES_DEFAULT_CATEGORY_CONFIG = {
    "settings": {"index": {"sort.field": ["id"], "sort.order": ["asc"]}},
    "mappings": {
        "properties": {
            "url_key": {"type": "keyword"},
            "redirect_url_key": {"type": "keyword"},
            "id": {"type": "integer"},
        }
    },
}

ES_DEFAULT_BRAND_CONFIG = {
    "settings": {"index": {"sort.field": ["id"], "sort.order": ["asc"]}},
    "mappings": {
        "properties": {
            "url_key": {"type": "keyword"},
            "redirect_url_key": {"type": "keyword"},
            "id": {"type": "integer"},
        }
    },
}
