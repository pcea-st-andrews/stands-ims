from datetime import date, timedelta

from django.test import SimpleTestCase, TestCase
from django.utils.module_loading import import_string

from people import constants, forms, validators
from people.factories import (
    AdultFactory,
    ChildFactory,
    InterpersonalRelationshipFactory,
    PersonFactory,
)
from people.utils import get_todays_adult_dob


class PersonFormTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.PersonForm()

    def test_fields(self):
        fields = self.form.fields.keys()
        self.assertEqual(list(fields), ["username", "full_name", "gender", "dob"])


class PersonFormFieldsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.PersonForm
        cls.form_fields = cls.form().fields
        cls.person = PersonFactory.build()
        cls.data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }


class PersonUsernameTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("username")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 25)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.contrib.auth.validators.UnicodeUsernameValidator"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_non_unique_value(self):
        # setup
        person = PersonFactory()
        data = self.data.copy()
        data["username"] = person.username

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"username": ["A person with that username already exists."]}
        self.assertEqual(form.errors, errors)

    def test_value_with_spaces(self):
        # setup
        data = self.data.copy()
        data["username"] = data["full_name"]

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        username_error = "Enter a valid username. This value may contain only letters, "
        username_error += "numbers, and @/./+/-/_ characters."
        self.assertEqual(form.errors, {"username": [username_error]})


class PersonFullNameTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("full_name")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 150)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_full_name"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_value_with_one_name(self):
        data = self.data.copy()
        data["full_name"] = data["username"]
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"full_name": [validators.INVALID_FULL_NAME_ERROR]}
        self.assertEqual(form.errors, errors)


class PersonGenderTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("gender")

    def test_choices(self):
        none_option = [("", "---------")]
        self.assertEqual(self.field.choices, none_option + constants.GENDER_CHOICES)

    def test_label(self):
        self.assertEqual(self.field.label, "Gender")

    def test_required(self):
        self.assertTrue(self.field.required)


class PersonDOBTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("dob")

    def test_label(self):
        self.assertEqual(self.field.label, "Date of birth")

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 1)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_date_of_birth"),
        )

    def test_date_in_future(self):
        # setup
        data = self.data.copy()
        data["dob"] = date.today() + timedelta(days=1)

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"dob": [validators.DOB_IN_FUTURE_ERROR]}
        self.assertEqual(form.errors, errors)

    def test_date_in_distant_past(self):
        # setup
        data = self.data.copy()
        days_lived = 365.25 * (constants.MAX_HUMAN_AGE + 1)
        data["dob"] = date.today() - timedelta(days=round(days_lived))

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"dob": [validators.DOB_IN_DISTANT_PAST_ERROR]}
        self.assertEqual(form.errors, errors)


class AdultFormTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.AdultForm()

    def test_fields(self):
        fields = self.form.fields.keys()
        self.assertEqual(list(fields), ["username", "full_name", "gender", "dob"])


class AdultFormFieldsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.AdultForm
        cls.form_fields = cls.form().fields
        cls.person = AdultFactory.build()
        cls.data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }


class AdultUsernameTestCase(AdultFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("username")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 25)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.contrib.auth.validators.UnicodeUsernameValidator"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_non_unique_value(self):
        # setup
        person = PersonFactory()
        data = self.data.copy()
        data["username"] = person.username

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"username": ["A person with that username already exists."]}
        self.assertEqual(form.errors, errors)

    def test_value_with_spaces(self):
        # setup
        data = self.data.copy()
        data["username"] = data["full_name"]

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        username_error = "Enter a valid username. This value may contain only letters, "
        username_error += "numbers, and @/./+/-/_ characters."
        self.assertEqual(form.errors, {"username": [username_error]})


class AdultFullNameTestCase(AdultFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("full_name")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 150)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_full_name"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_value_with_one_name(self):
        data = self.data.copy()
        data["full_name"] = data["username"]
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"full_name": [validators.INVALID_FULL_NAME_ERROR]}
        self.assertEqual(form.errors, errors)


class AdultGenderTestCase(AdultFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("gender")

    def test_choices(self):
        none_option = [("", "---------")]
        self.assertEqual(self.field.choices, none_option + constants.GENDER_CHOICES)

    def test_label(self):
        self.assertEqual(self.field.label, "Gender")

    def test_required(self):
        self.assertTrue(self.field.required)


class AdultDOBTestCase(AdultFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("dob")

    def test_label(self):
        self.assertEqual(self.field.label, "Date of birth")

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 2)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_date_of_birth"),
        )
        self.assertEqual(
            self.field.validators[1],
            import_string("people.validators.validate_adult"),
        )

    def test_date_in_future(self):
        # setup
        data = self.data.copy()
        data["dob"] = date.today() + timedelta(days=1)

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        dob_errors = form.errors.get("dob")
        self.assertEqual(len(dob_errors), 2)
        self.assertEqual(dob_errors[0], validators.DOB_IN_FUTURE_ERROR)

    def test_date_in_distant_past(self):
        # setup
        data = self.data.copy()
        days_lived = 365.25 * (constants.MAX_HUMAN_AGE + 1)
        data["dob"] = date.today() - timedelta(days=round(days_lived))

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"dob": [validators.DOB_IN_DISTANT_PAST_ERROR]}
        self.assertEqual(form.errors, errors)

    def test_child_dob(self):
        # setup
        data = self.data.copy()
        data["dob"] = ChildFactory.build().dob

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"dob": [f"Date of birth must be before {get_todays_adult_dob()}"]}
        self.assertEqual(form.errors, errors)


class ChildFormTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.ChildForm()

    def test_fields(self):
        fields = self.form.fields.keys()
        self.assertEqual(list(fields), ["username", "full_name", "gender", "dob"])


class ChildFormFieldsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.ChildForm
        cls.form_fields = cls.form().fields
        cls.person = ChildFactory.build()
        cls.data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }


class ChildUsernameTestCase(ChildFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("username")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 25)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.contrib.auth.validators.UnicodeUsernameValidator"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_non_unique_value(self):
        # setup
        person = PersonFactory()
        data = self.data.copy()
        data["username"] = person.username

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"username": ["A person with that username already exists."]}
        self.assertEqual(form.errors, errors)

    def test_value_with_spaces(self):
        # setup
        data = self.data.copy()
        data["username"] = data["full_name"]

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        username_error = "Enter a valid username. This value may contain only letters, "
        username_error += "numbers, and @/./+/-/_ characters."
        self.assertEqual(form.errors, {"username": [username_error]})


class ChildFullNameTestCase(ChildFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("full_name")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 150)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_full_name"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_value_with_one_name(self):
        data = self.data.copy()
        data["full_name"] = data["username"]
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"full_name": [validators.INVALID_FULL_NAME_ERROR]}
        self.assertEqual(form.errors, errors)


class ChildGenderTestCase(ChildFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("gender")

    def test_choices(self):
        none_option = [("", "---------")]
        self.assertEqual(self.field.choices, none_option + constants.GENDER_CHOICES)

    def test_label(self):
        self.assertEqual(self.field.label, "Gender")

    def test_required(self):
        self.assertTrue(self.field.required)


class ChildDOBTestCase(ChildFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("dob")

    def test_label(self):
        self.assertEqual(self.field.label, "Date of birth")

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 2)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_date_of_birth"),
        )
        self.assertEqual(
            self.field.validators[1],
            import_string("people.validators.validate_child"),
        )

    def test_date_in_future(self):
        # setup
        data = self.data.copy()
        data["dob"] = date.today() + timedelta(days=1)

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"dob": [validators.DOB_IN_FUTURE_ERROR]}
        self.assertEqual(form.errors, errors)

    def test_date_in_distant_past(self):
        # setup
        data = self.data.copy()
        days_lived = 365.25 * (constants.MAX_HUMAN_AGE + 1)
        data["dob"] = date.today() - timedelta(days=round(days_lived))

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        dob_errors = form.errors.get("dob")
        self.assertEqual(len(dob_errors), 2)
        self.assertEqual(dob_errors[0], validators.DOB_IN_DISTANT_PAST_ERROR)

    def test_adult_dob(self):
        # setup
        data = self.data.copy()
        data["dob"] = AdultFactory.build().dob

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"dob": [f"Date of birth must be after {get_todays_adult_dob()}"]}
        self.assertEqual(form.errors, errors)


class InterpersonalRelationshipCreationFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.InterpersonalRelationshipCreationForm()

    def test_fields(self):
        fields = self.form.fields.keys()
        self.assertEqual(list(fields), ["person", "relative", "relation"])

    def test_self_relationship(self):
        username = PersonFactory().username
        relationship = InterpersonalRelationshipFactory.build().relation
        data = {"person": username, "relative": username, "relation": relationship}
        form = forms.InterpersonalRelationshipCreationForm(data=data)
        self.assertFalse(form.is_valid())
        errors = {"__all__": [forms.SELF_RELATIONSHIPS_ERROR]}
        self.assertEqual(form.errors, errors)

    def test_duplicate_relationship(self):
        relationship = InterpersonalRelationshipFactory()
        data = {
            "person": relationship.person.username,
            "relative": relationship.relative.username,
            "relation": relationship.relation,
        }
        form = forms.InterpersonalRelationshipCreationForm(data=data)
        self.assertFalse(form.is_valid())
        errors = {"__all__": [forms.DUPLICATE_RELATIONSHIPS_ERROR]}
        self.assertEqual(form.errors, errors)


class InterpersonalRelationshipCreationFormFieldsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = forms.InterpersonalRelationshipCreationForm
        cls.form_fields = cls.form().fields
        cls.person = PersonFactory()
        cls.relative = PersonFactory()
        cls.relation = InterpersonalRelationshipFactory.build().relation
        cls.data = {
            "person": str(cls.person.username),
            "relative": str(cls.relative.username),
            "relation": cls.relation,
        }


class InterpersonalRelationshipPersonTestCase(
    InterpersonalRelationshipCreationFormFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("person")

    def test_label(self):
        self.assertEqual(self.field.label, "The person's username")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 25)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_person_username"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_non_existent_person(self):
        data = self.data.copy()
        data["person"] = "does-not-exist"
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {
            "person": [
                validators.PERSON_DOES_NOT_EXIST_ERROR % dict(username=data["person"])
            ]
        }
        self.assertEqual(form.errors, errors)


class InterpersonalRelationshipRelativeTestCase(
    InterpersonalRelationshipCreationFormFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("relative")

    def test_label(self):
        self.assertEqual(self.field.label, "The relative's username")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 25)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_person_username"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_non_existent_person(self):
        data = self.data.copy()
        data["relative"] = "does-not-exist"
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {
            "relative": [
                validators.PERSON_DOES_NOT_EXIST_ERROR % dict(username=data["relative"])
            ]
        }
        self.assertEqual(form.errors, errors)


class InterpersonalRelationshipRelationTestCase(
    InterpersonalRelationshipCreationFormFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("relation")

    def test_choices(self):
        self.assertEqual(
            self.field.choices, constants.INTERPERSONAL_RELATIONSHIP_CHOICES
        )

    def test_initial(self):
        self.assertEqual(self.field.initial, constants.FAMILIAL_RELATIONSHIPS[0])

    def test_label(self):
        self.assertEqual(self.field.label, "Relationship type")

    def test_required(self):
        self.assertTrue(self.field.required)
