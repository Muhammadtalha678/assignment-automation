import { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, ImageRun, HeadingLevel, BorderStyle } from 'docx';

interface AssignmentPayload {
  assignment_no: number;
  course_code: number;
  semester: string;
  student_name: string;
  registration_id: string;
  questions: string[];
  language: string;
}

export async function generateDemoDocxBlob(payload: AssignmentPayload, logoFile: File | null): Promise<Blob> {
  let logoImageRun: ImageRun | null = null;

  if (logoFile) {
    try {
      const buffer = await logoFile.arrayBuffer();
      logoImageRun = new ImageRun({
        data: buffer,
        transformation: {
          width: 120,
          height: 120,
        },
        type: logoFile.type === 'image/png' ? 'png' : 'jpg',
      });
    } catch (e) {
      console.warn("Could not parse logo file for docx", e);
    }
  }

  const isUrdu = payload.language === 'Urdu';

  const children: any[] = [];

  // Logo if available
  if (logoImageRun) {
    children.push(
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [logoImageRun],
        spacing: { after: 200 },
      })
    );
  }

  // Header Title
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      heading: HeadingLevel.TITLE,
      children: [
        new TextRun({
          text: isUrdu ? "اسائنمنٹ کور پیج" : "ASSIGNMENT COVER SHEET",
          bold: true,
          size: 32,
          color: "1E3A8A",
        }),
      ],
      spacing: { after: 300 },
    })
  );

  // Metadata Table
  const tableRows = [
    ["Language / زبان", payload.language],
    ["Assignment No / اسائنمنٹ نمبر", String(payload.assignment_no)],
    ["Course Code / کورس کوڈ", String(payload.course_code)],
    ["Semester / سمسٹر", payload.semester],
    ["Student Name / طالب علم کا نام", payload.student_name],
    ["Registration ID / رجسٹریشن آئی ڈی", payload.registration_id],
  ];

  const table = new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: tableRows.map(([label, val]) => 
      new TableRow({
        children: [
          new TableCell({
            width: { size: 40, type: WidthType.PERCENTAGE },
            children: [new Paragraph({ children: [new TextRun({ text: label, bold: true, size: 22 })] })],
            shading: { fill: "F1F5F9" },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
              left: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
              right: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
            }
          }),
          new TableCell({
            width: { size: 60, type: WidthType.PERCENTAGE },
            children: [new Paragraph({ children: [new TextRun({ text: val, size: 22 })] })],
            borders: {
              top: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
              left: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
              right: { style: BorderStyle.SINGLE, size: 1, color: "CBD5E1" },
            }
          }),
        ]
      })
    ),
  });

  children.push(table);

  // Section Header for Questions
  children.push(
    new Paragraph({
      heading: HeadingLevel.HEADING_2,
      children: [
        new TextRun({
          text: isUrdu ? "سوالات (Questions)" : "ASSIGNMENT QUESTIONS",
          bold: true,
          size: 26,
          color: "1E3A8A",
        }),
      ],
      spacing: { before: 400, after: 200 },
    })
  );

  // List of Questions
  payload.questions.forEach((q, idx) => {
    children.push(
      new Paragraph({
        children: [
          new TextRun({
            text: `Q${idx + 1}: `,
            bold: true,
            color: "2563EB",
            size: 24,
          }),
          new TextRun({
            text: q,
            size: 24,
          }),
        ],
        spacing: { after: 150 },
      })
    );
  });

  const doc = new Document({
    sections: [
      {
        properties: {},
        children: children,
      },
    ],
  });

  return await Packer.toBlob(doc);
}
