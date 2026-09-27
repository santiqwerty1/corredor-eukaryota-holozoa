// QA de lectura, sin escribir el corpus ni modificar el runtime empaquetado.
import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

const [modulePath, root, expectedPath] = process.argv.slice(2);
const { Workbook } = await import(pathToFileURL(modulePath).href);
const expected = JSON.parse(await fs.readFile(expectedPath, 'utf8'));
const sha = value => createHash('sha256').update(value).digest('hex');
const records = [];
for (const item of expected) {
  const bytes = await fs.readFile(path.join(root, item.path));
  if (sha(bytes) !== item.sha256_csv) throw new Error(`Entrada cambió: ${item.path}`);
  const workbook = await Workbook.fromCSV(bytes.toString('utf8'), {sheetName: 'Datos'});
  const values = workbook.worksheets.getItem('Datos').getUsedRange().values;
  const digest = sha(JSON.stringify(values));
  const rows = values.length;
  const widths = [...new Set(values.map(row => row.length))];
  const conforming = digest === item.sha256_matrix && rows === item.rows
    && widths.length === 1 && widths[0] === item.columns;
  records.push({...item, observed_rows: rows, observed_columns: widths,
    sha256_observed_matrix: digest, result: conforming ? 'CONFORME' : 'NO_CONFORME'});
}
console.log(JSON.stringify({
  method: 'CSV importado por Workbook.fromCSV; comparación exacta de cada celda contra csv.reader; sin conversiones',
  node: process.version,
  expected_sha256: sha(await fs.readFile(expectedPath)),
  total: records.length,
  failures: records.filter(row => row.result !== 'CONFORME').length,
  records,
}, null, 2));
if (records.some(row => row.result !== 'CONFORME')) process.exitCode = 1;
