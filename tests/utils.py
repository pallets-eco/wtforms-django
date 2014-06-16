from wtforms.compat import text_type


def contains_validator(field, v_type):
    for v in field.validators:
        if isinstance(v, v_type):
            return True
    return False


def lazy_select(field, **kwargs):
    output = []
    for val, label, selected in field.iter_choices():
        s = selected and 'Y' or 'N'
        output.append('%s:%s:%s' % (s, text_type(val), text_type(label)))
    return tuple(output)


class DummyPostData(dict):
    def getlist(self, key):
        return self[key]
