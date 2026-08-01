import unittest
from models import (
    Page,
    Row,
    Column,
    TextBlock,
    ImageBlock,
    ButtonBlock,
    AlertBlock,
    HtmlBlock,
    TableBlock,
    CardBlock,
    BadgeBlock,
    AccordionBlock,
    ListGroupBlock,
)
from generator import HTMLGenerator
import security


class TestBootstrapGenerator(unittest.TestCase):
    def test_model_hierarchy_and_rendering(self):
        # 1. Erstelle Hierarchie
        page = Page("Test Seite")
        row = Row()
        col = Column(6)

        text = TextBlock("Hallo Welt")
        img = ImageBlock("http://example.com/bild.jpg", "Test Bild")
        btn = ButtonBlock("Jetzt anfragen", "http://example.com", "success")
        alert = AlertBlock("Achtung wichtigen Hinweis!", "warning")
        custom_html = HtmlBlock('<span class="badge bg-primary">Custom HTML</span>')

        col.add_element(text)
        col.add_element(img)
        col.add_element(btn)
        col.add_element(alert)
        col.add_element(custom_html)
        row.add_column(col)
        page.add_row(row)

        # 2. Render Check
        rendered_html = HTMLGenerator.generate_html(page)

        self.assertIn("Test Seite", rendered_html)
        self.assertIn('class="row mb-3"', rendered_html)
        self.assertIn('class="col-md-6"', rendered_html)
        self.assertIn("<p>Hallo Welt</p>", rendered_html)
        self.assertIn('src="http://example.com/bild.jpg"', rendered_html)
        self.assertIn('class="btn btn-success"', rendered_html)
        self.assertIn('class="alert alert-warning"', rendered_html)
        self.assertIn(
            '<span class="badge bg-primary">Custom HTML</span>', rendered_html
        )

    def test_bootstrap_3_rendering(self):
        page = Page("BS3 Seite")
        row = Row()
        col = Column(12)
        col.add_element(ImageBlock("http://example.com/b3.jpg"))
        row.add_column(col)
        page.add_row(row)

        rendered_html = HTMLGenerator.generate_html(page, bootstrap_version="3")
        self.assertIn("bootstrap.min.css", rendered_html)
        self.assertIn("jquery-1.12.4.min.js", rendered_html)
        self.assertIn('class="img-responsive"', rendered_html)
        self.assertIn('class="row"', rendered_html)

    def test_serialization_deserialization(self):
        page = Page("Speicher Test")
        row = Row()
        col = Column(12)
        col.add_element(TextBlock("Persistenz Text"))
        col.add_element(ButtonBlock("Klick", "http://test.de", "primary"))
        col.add_element(AlertBlock("Info Text", "info"))
        row.add_column(col)
        page.add_row(row)

        data_dict = page.to_dict()

        # Test serialization format
        self.assertEqual(data_dict["title"], "Speicher Test")
        self.assertEqual(len(data_dict["rows"]), 1)
        self.assertEqual(
            data_dict["rows"][0]["columns"][0]["elements"][0]["text"], "Persistenz Text"
        )
        self.assertEqual(
            data_dict["rows"][0]["columns"][0]["elements"][1]["type"], "ButtonBlock"
        )
        self.assertEqual(
            data_dict["rows"][0]["columns"][0]["elements"][2]["type"], "AlertBlock"
        )

        # Test from_dict
        new_page = Page.from_dict(data_dict)
        self.assertEqual(new_page.title, "Speicher Test")
        self.assertEqual(len(new_page.rows), 1)

        restored_elements = new_page.rows[0].columns[0].elements
        self.assertEqual(restored_elements[0].text, "Persistenz Text")
        self.assertEqual(restored_elements[1].text, "Klick")
        self.assertEqual(restored_elements[2].style, "info")

    def test_security_encryption_decryption(self):
        dummy_data = {"test_key": "geheime_daten_123"}
        password = "SuperSicheresPassword!123"

        # Verschlüsseln
        encrypted = security.encrypt_project(dummy_data, password)
        self.assertNotEqual(str(dummy_data).encode(), encrypted)

        # Entschlüsseln mit richtigem Passwort
        decrypted = security.decrypt_project(encrypted, password)
        self.assertEqual(decrypted["test_key"], "geheime_daten_123")

        # Entschlüsseln mit falschem Passwort (muss Exception werfen)
        with self.assertRaises(ValueError):
            security.decrypt_project(encrypted, "FalschesPasswort")

    def test_converter_bs3_to_bs5(self):
        from generator import HTMLConverter

        bs3_code = '<img src="#" alt="text" class="img-responsive center-block>'
        converted = HTMLConverter.convert_bs3_to_bs5(bs3_code)

        self.assertIn('class="img-fluid mx-auto d-block"', converted)
        self.assertTrue(converted.endswith("/>"))

    def test_new_bootstrap_blocks(self):
        page = Page("Neue Blöcke Test")
        row = Row()
        col = Column(12)

        col.add_element(TableBlock(headers=["A", "B"], rows=[["1", "2"]]))
        col.add_element(
            CardBlock(title="Card Header", content="Card Body", style="primary")
        )
        col.add_element(BadgeBlock(text="Neu", style="danger"))
        col.add_element(
            AccordionBlock(items=[{"title": "Acc 1", "content": "Inhalt 1"}])
        )
        col.add_element(ListGroupBlock(items=["Punkt 1", "Punkt 2"]))

        row.add_column(col)
        page.add_row(row)

        # BS5 Check
        html_bs5 = HTMLGenerator.generate_html(page, bootstrap_version="5")
        self.assertIn('<table class="table table-striped table-hover">', html_bs5)
        self.assertIn('<div class="card text-bg-primary mb-3">', html_bs5)
        self.assertIn('<span class="badge bg-danger">Neu</span>', html_bs5)
        self.assertIn('class="accordion"', html_bs5)
        self.assertIn('<ul class="list-group">', html_bs5)

        # BS3 Check
        html_bs3 = HTMLGenerator.generate_html(page, bootstrap_version="3")
        self.assertIn('<div class="panel panel-primary">', html_bs3)
        self.assertIn('<span class="label label-danger">Neu</span>', html_bs3)
        self.assertIn('class="panel-group"', html_bs3)

    def test_element_spacing(self):
        btn = ButtonBlock(
            "Klick",
            margin_top="3",
            margin_bottom="2",
            padding_top="1",
            padding_bottom="4",
        )
        html_rendered = btn.apply_spacing_to_html(btn.render())
        self.assertIn('<div class="mt-3 mb-2 pt-1 pb-4">', html_rendered)

    def test_parse_html_table(self):
        from generator import HTMLConverter

        raw_table_html = """
        <table class="table">
            <thead>
                <tr><th>Name</th><th>Alter</th><th>Stadt</th></tr>
            </thead>
            <tbody>
                <tr><td>Anna</td><td>28</td><td>Berlin</td></tr>
                <tr><td>Ben</td><td>35</td><td>München</td></tr>
            </tbody>
        </table>
        """
        headers, rows = HTMLConverter.parse_html_table(raw_table_html)
        self.assertEqual(headers, ["Name", "Alter", "Stadt"])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["Anna", "28", "Berlin"])

    def test_xss_protection(self):
        img = ImageBlock(
            url='http://test.de/" onload="alert(1)"', alt='Bild " onerror="alert(1)"'
        )
        rendered_img = img.render()
        self.assertNotIn('onload="alert(1)"', rendered_img)
        self.assertIn("&quot;", rendered_img)

        btn = ButtonBlock(text="Klick", style="primary; background:red")
        rendered_btn = btn.render()
        self.assertIn('class="btn btn-primarybackgroundred"', rendered_btn)


if __name__ == "__main__":
    unittest.main()
