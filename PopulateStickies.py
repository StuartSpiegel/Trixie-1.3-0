from lxml import etree

w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
v = "{urn:schemas-microsoft-com:vml}"
a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def populate_category(paragraph, category):
    # Paragraph spacing
    for paragraphStyle in paragraph.iter(w + "pPr"):
        etree.SubElement(paragraphStyle, w + "spacing",
                         attrib={w + "before": "100", w + "beforeAutospacing": "1", w + "after": "100",
                                 w + "afterAutospacing": "1", w + "line": "240", w + "lineRule": "auto"})
        etree.SubElement(paragraphStyle, w + "outlineLevel", attrib={w + "val": "2"})

    # Create new Run
    run = etree.Element(w + "r")
    run.attrib[w + "rsidRPr"] = "00143C72"

    # Create Run style
    runStyle = etree.Element(w + "rPr")
    etree.SubElement(runStyle, w + "rFonts",
                     attrib={w + "ascii": "Times New Roman", w + "eastAsia": "Times New Roman",
                             w + "hAnsi": "Times New Roman", w + "cs": "Times New Roman"})
    etree.SubElement(runStyle, w + "b")
    etree.SubElement(runStyle, w + "bCs")
    etree.SubElement(runStyle, w + "sz", attrib={w + "val": "28"})
    etree.SubElement(runStyle, w + "szCs", attrib={w + "val": "28"})
    run.insert(0, runStyle)

    # Create text in the run
    text = etree.Element(w + "t")
    # text.attrib["xml:space"] = "preserve"
    text.text = category
    run.insert(1, text)

    # Insert Run into current XML
    paragraph.insert(1, run)


def populate_title(feature, run):
    for txbx in run.iter(w + "txbxContent"):
        for paragraph in txbx.iter(w + "p"):
            subRun = etree.Element(w + "r")
            text = etree.Element(w + "t")
            text.text = feature
            subRun.insert(0, text)
            paragraph.insert(1, subRun)


def populate_color(run, color):
    for fillColor in run.iter(a + "srgbClr"):
        fillColor.attrib["val"] = color
    for rect in run.iter(v + "rect"):
        rect.attrib["fillcolor"] = "#" + color


def populate_points(points, run):
    for txbx in run.iter(w + "txbxContent"):
        for paragraph in txbx.iter(w + "p"):
            subRun = etree.Element(w + "r")
            text = etree.Element(w + "t")
            text.text = points
            subRun.insert(0, text)

            # Add formatting
            rPr = etree.Element(w + "rPr")
            etree.SubElement(rPr, w + "sz", attrib={w + "val": "40"})
            subRun.insert(0, rPr)

            paragraph.insert(1, subRun)


# This is the default population method
def populate_text(run, storyCategory, storyDescription, storyBullets, acceptanceCriteria):
    for txbx in run.iter(w + "txbxContent"):
        # Add story category to first existing paragraph
        for subParagraph in txbx.iter(w + "p"):
            populate_category(subParagraph, storyCategory)
            break
        # Populates the text with the requested acceptance Criteria
        for subParagraph in txbx.iter(w + "p"):
            populate_category(subParagraph, acceptanceCriteria)
            break
        # Add new paragraph containing the story points
        content = etree.Element(w + "p",
                                attrib={w + "rsidR": "0014164D", w + "rsidRPr": "00DB3E27",
                                        w + "rsidRDefault": "00143C72", w + "rsidP": "00DB3E27"})
        # Inserting the story description
        newRun = etree.Element(w + "r")
        newText = etree.Element(w + "t")
        newText.text = storyDescription
        newRun.insert(0, newText)

        # Inserting the acceptance Criteria
        acceptanceText = etree.Element(w + "t")
        acceptanceText.text = acceptanceCriteria
        newRun.insert(1, acceptanceText)  # added
        content.insert(0, newRun)
        txbx.insert(1, content)  # -Flag

        # If there are bullets, add new paragraphs for them (add story point bullets)
        for i, bulletText in zip(range(len(storyBullets)), storyBullets):
            bullet = etree.Element(w + "p",
                                   attrib={w + "rsidR": "00924485", w + "rsidRPr": "00924485",
                                           w + "rsidRDefault": "00924485", w + "rsidP": "002853AF"})  # 00524C8F
            # Add paragraph formatting
            pPr = etree.Element(w + "pPr")
            numPr = etree.Element(w + "numPr")
            etree.SubElement(numPr, w + "ilvl", attrib={w + "val": "0"})
            etree.SubElement(numPr, w + "numId", attrib={w + "val": "11"})
            etree.SubElement(pPr, w + "pStyle", attrib={w + "val": "ListParagraph"})
            pPr.insert(0, numPr)
            etree.SubElement(pPr, w + "spacing",
                             attrib={w + "before": "100", w + "beforeAutospacing": "1", w + "after": "100",
                                     w + "afterAutospacing": "1", w + "line": "240", w + "lineRule": "auto"})
            bullet.insert(0, pPr)

            # Add run
            newRun = etree.Element(w + "r", attrib={w + "rsidRPr": "002853AF"})

            # Run formatting
            rPr = etree.Element(w + "rPr")
            etree.SubElement(rPr, w + "rFonts",
                             attrib={w + "ascii": "Times New Roman", w + "eastAsia": "Times New Roman",
                                     w + "hAnsi": "Times New Roman", w + "cs": "Times New Roman"})
            etree.SubElement(rPr, w + "sz", attrib={w + "val": "24"})
            etree.SubElement(rPr, w + "szCs", attrib={w + "val": "24"})
            newRun.insert(0, rPr)

            # Run text
            newText = etree.Element(w + "t")
            newText.text = bulletText
            newRun.insert(1, newText)
            bullet.insert(1, newRun)
            txbx.insert(-1, bullet)

# ----------------------------------------------------------------------------------------------------------------------#
