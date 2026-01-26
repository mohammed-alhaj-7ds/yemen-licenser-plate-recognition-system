import { useState } from 'react';
import Button from './Button';
import './PlateNumberCard.css';

const NO_PLATE_MESSAGE = '❌ لم يتم العثور على لوحة ترخيص في الصورة';
const NO_PLATE_SUGGESTIONS = [
  'استخدم صورة أوضح للوحة',
  'تأكد أن اللوحة ظاهرة بالكامل في الإطار',
  'حسّن الإضاءة وتجنب الانعكاس',
];

function PlateNumberCard({ plate, index }) {
  const [copied, setCopied] = useState(false);

  const getPlateNumber = () => {
    const candidates = [
      plate.plate_number,
      plate.car_number,
      plate.raw_ocr,
      plate.number,
      plate.plate,
    ];
    const invalid = ['unknown', 'null', 'undefined', ''];

    for (const candidate of candidates) {
      if (candidate && typeof candidate === 'string' && candidate.trim().length > 0) {
        const t = candidate.trim().toLowerCase();
        if (!invalid.includes(t)) return candidate.trim();
      }
    }

    if (plate.raw_reads && Array.isArray(plate.raw_reads) && plate.raw_reads.length > 0) {
      const valid = plate.raw_reads
        .filter(r => r?.digits && typeof r.digits === 'string' && r.digits.trim().length >= 3)
        .sort((a, b) => (b.confidence || 0) - (a.confidence || 0));
      if (valid.length > 0 && valid[0].digits) return valid[0].digits.trim();
    }

    return null;
  };

  const plateNumber = getPlateNumber();
  const hasPlateNumber = !!plateNumber;

  const handleCopy = () => {
    if (plateNumber) {
      navigator.clipboard.writeText(plateNumber);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className={`plate-number-card ${hasPlateNumber ? 'has-number' : 'no-number'}`}>
      <div className="plate-number-card-header">
        <div className="plate-number-label">
          <span className="label-icon">🚗</span>
          <span className="label-text">رقم اللوحة</span>
        </div>
        <div className="plate-number-badge">لوحة #{index + 1}</div>
      </div>

      <div className="plate-number-display">
        {hasPlateNumber ? (
          <>
            <div className="plate-number-value">{plateNumber}</div>
            <Button
              variant="outline"
              size="small"
              onClick={handleCopy}
              icon={copied ? '✅' : '📋'}
            >
              {copied ? 'تم النسخ' : 'نسخ'}
            </Button>
          </>
        ) : (
          <div className="plate-number-missing">
            <div className="missing-message">{NO_PLATE_MESSAGE}</div>
            <ul className="missing-suggestions">
              {NO_PLATE_SUGGESTIONS.map((s, i) => (
                <li key={i}>
                  <span className="suggestion-icon">ℹ️</span>
                  {s}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default PlateNumberCard;
