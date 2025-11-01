export const exportToCSV = (emails, filename = 'jobmail_insight.csv') => {
  const headers = ['Company', 'Subject', 'Status', 'Date', 'Sender'];
  const rows = emails.map(e => [
    e.company,
    `"${e.subject.replace(/"/g, '""')}"`,
    e.status,
    e.date,
    `"${e.sender.replace(/"/g, '""')}"`
  ]);
  
  const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  window.URL.revokeObjectURL(url);
};