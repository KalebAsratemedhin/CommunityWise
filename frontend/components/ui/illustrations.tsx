export function RAGIllustration() {
  return (
    <svg
      viewBox="0 0 400 300"
      className="w-full h-full"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Document stack */}
      <rect x="80" y="120" width="80" height="100" rx="4" fill="currentColor" opacity="0.1" />
      <rect x="90" y="110" width="80" height="100" rx="4" fill="currentColor" opacity="0.15" />
      <rect x="100" y="100" width="80" height="100" rx="4" fill="currentColor" opacity="0.2" />
      <path
        d="M110 130 L140 130 M110 145 L160 145 M110 160 L150 160"
        stroke="currentColor"
        strokeWidth="2"
        opacity="0.3"
      />
      
      {/* AI Brain/Circuit */}
      <circle cx="280" cy="150" r="60" fill="none" stroke="currentColor" strokeWidth="3" opacity="0.2" />
      <circle cx="260" cy="130" r="8" fill="currentColor" opacity="0.4" />
      <circle cx="300" cy="130" r="8" fill="currentColor" opacity="0.4" />
      <circle cx="270" cy="160" r="8" fill="currentColor" opacity="0.4" />
      <circle cx="290" cy="170" r="8" fill="currentColor" opacity="0.4" />
      <path
        d="M260 130 L270 160 M300 130 L290 170 M270 160 L290 170"
        stroke="currentColor"
        strokeWidth="2"
        opacity="0.3"
      />
      
      {/* Search/Connection lines */}
      <path
        d="M180 150 Q230 140 250 150"
        stroke="currentColor"
        strokeWidth="2"
        opacity="0.3"
        strokeDasharray="4 4"
      />
      
      {/* Community/Network nodes */}
      <circle cx="120" cy="60" r="15" fill="currentColor" opacity="0.2" />
      <circle cx="180" cy="50" r="15" fill="currentColor" opacity="0.2" />
      <circle cx="240" cy="60" r="15" fill="currentColor" opacity="0.2" />
      <path
        d="M120 60 L180 50 L240 60"
        stroke="currentColor"
        strokeWidth="2"
        opacity="0.2"
      />
    </svg>
  );
}

export function CommunityIllustration() {
  return (
    <svg
      viewBox="0 0 400 300"
      className="w-full h-full"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* People/Users */}
      <circle cx="120" cy="180" r="30" fill="currentColor" opacity="0.1" />
      <rect x="100" y="210" width="40" height="50" rx="20" fill="currentColor" opacity="0.1" />
      
      <circle cx="200" cy="170" r="35" fill="currentColor" opacity="0.15" />
      <rect x="177" y="205" width="46" height="55" rx="23" fill="currentColor" opacity="0.15" />
      
      <circle cx="280" cy="180" r="30" fill="currentColor" opacity="0.1" />
      <rect x="260" y="210" width="40" height="50" rx="20" fill="currentColor" opacity="0.1" />
      
      {/* Connection/Network lines */}
      <path
        d="M150 180 Q200 150 250 180"
        stroke="currentColor"
        strokeWidth="3"
        opacity="0.2"
      />
      
      {/* Knowledge/Document icon in center */}
      <rect x="185" y="110" width="30" height="40" rx="2" fill="currentColor" opacity="0.2" />
      <path
        d="M190 125 L210 125 M190 135 L205 135 M190 145 L200 145"
        stroke="currentColor"
        strokeWidth="2"
        opacity="0.3"
      />
      
      {/* Chat bubbles */}
      <ellipse cx="90" cy="140" rx="25" ry="15" fill="currentColor" opacity="0.1" />
      <ellipse cx="310" cy="140" rx="25" ry="15" fill="currentColor" opacity="0.1" />
    </svg>
  );
}

export function TechIllustration() {
  return (
    <svg
      viewBox="0 0 400 300"
      className="w-full h-full"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Server/Cloud */}
      <rect x="150" y="120" width="100" height="80" rx="4" fill="currentColor" opacity="0.1" />
      <rect x="160" y="130" width="80" height="8" rx="2" fill="currentColor" opacity="0.2" />
      <rect x="160" y="150" width="80" height="8" rx="2" fill="currentColor" opacity="0.2" />
      <rect x="160" y="170" width="60" height="8" rx="2" fill="currentColor" opacity="0.2" />
      
      {/* Data flow */}
      <path
        d="M100 160 L150 160 M250 160 L300 160"
        stroke="currentColor"
        strokeWidth="3"
        opacity="0.3"
      />
      <circle cx="100" cy="160" r="8" fill="currentColor" opacity="0.3" />
      <circle cx="300" cy="160" r="8" fill="currentColor" opacity="0.3" />
      
      {/* AI nodes */}
      <circle cx="120" cy="80" r="20" fill="currentColor" opacity="0.15" />
      <circle cx="200" cy="60" r="25" fill="currentColor" opacity="0.2" />
      <circle cx="280" cy="80" r="20" fill="currentColor" opacity="0.15" />
      
      {/* Connection network */}
      <path
        d="M120 80 L200 60 L280 80"
        stroke="currentColor"
        strokeWidth="2"
        opacity="0.2"
      />
      <path
        d="M120 80 L150 140 M280 80 L250 140"
        stroke="currentColor"
        strokeWidth="2"
        opacity="0.2"
      />
      
      {/* Database/Storage */}
      <ellipse cx="200" cy="240" rx="60" ry="15" fill="currentColor" opacity="0.1" />
      <ellipse cx="200" cy="230" rx="50" ry="12" fill="currentColor" opacity="0.15" />
    </svg>
  );
}

export function ColorfulAIIllustration() {
  return (
    <svg
      viewBox="0 0 400 300"
      className="w-full h-full"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Colorful AI Brain */}
      <circle cx="200" cy="150" r="70" fill="#4A90E2" opacity="0.2" />
      <circle cx="200" cy="150" r="50" fill="#E94B3C" opacity="0.15" />
      
      {/* Colorful nodes */}
      <circle cx="170" cy="120" r="12" fill="#4A90E2" />
      <circle cx="230" cy="120" r="12" fill="#E94B3C" />
      <circle cx="160" cy="160" r="12" fill="#F5A623" />
      <circle cx="240" cy="160" r="12" fill="#7B68EE" />
      <circle cx="185" cy="180" r="12" fill="#50C878" />
      <circle cx="215" cy="180" r="12" fill="#FF6B9D" />
      
      {/* Connection lines */}
      <path d="M170 120 L185 180" stroke="#4A90E2" strokeWidth="2" opacity="0.4" />
      <path d="M230 120 L215 180" stroke="#E94B3C" strokeWidth="2" opacity="0.4" />
      <path d="M160 160 L185 180" stroke="#F5A623" strokeWidth="2" opacity="0.4" />
      <path d="M240 160 L215 180" stroke="#7B68EE" strokeWidth="2" opacity="0.4" />
    </svg>
  );
}

export function ColorfulCommunityIllustration() {
  return (
    <svg
      viewBox="0 0 400 300"
      className="w-full h-full"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Colorful people/avatars */}
      <circle cx="120" cy="180" r="25" fill="#4A90E2" />
      <rect x="100" y="205" width="40" height="45" rx="20" fill="#4A90E2" opacity="0.7" />
      
      <circle cx="200" cy="170" r="28" fill="#E94B3C" />
      <rect x="175" y="198" width="50" height="50" rx="25" fill="#E94B3C" opacity="0.7" />
      
      <circle cx="280" cy="180" r="25" fill="#50C878" />
      <rect x="260" y="205" width="40" height="45" rx="20" fill="#50C878" opacity="0.7" />
      
      {/* Colorful connection lines */}
      <path d="M145 180 Q200 150 255 180" stroke="#F5A623" strokeWidth="4" opacity="0.6" />
      
      {/* Colorful chat bubbles */}
      <ellipse cx="90" cy="130" rx="20" ry="12" fill="#7B68EE" opacity="0.6" />
      <ellipse cx="310" cy="130" rx="20" ry="12" fill="#FF6B9D" opacity="0.6" />
      
      {/* Center knowledge icon */}
      <rect x="185" y="100" width="30" height="40" rx="3" fill="#F5A623" opacity="0.4" />
      <path d="M190 115 L210 115 M190 125 L205 125 M190 135 L200 135" stroke="#F5A623" strokeWidth="2" />
    </svg>
  );
}

export function ColorfulDocumentIllustration() {
  return (
    <svg
      viewBox="0 0 400 300"
      className="w-full h-full"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Colorful document stack */}
      <rect x="80" y="140" width="90" height="110" rx="5" fill="#E94B3C" opacity="0.2" />
      <rect x="90" y="130" width="90" height="110" rx="5" fill="#4A90E2" opacity="0.25" />
      <rect x="100" y="120" width="90" height="110" rx="5" fill="#50C878" opacity="0.3" />
      
      {/* Document lines */}
      <path d="M110 150 L180 150" stroke="#50C878" strokeWidth="2" opacity="0.5" />
      <path d="M110 165 L170 165" stroke="#50C878" strokeWidth="2" opacity="0.5" />
      <path d="M110 180 L160 180" stroke="#50C878" strokeWidth="2" opacity="0.5" />
      <path d="M110 195 L175 195" stroke="#50C878" strokeWidth="2" opacity="0.5" />
      
      {/* Colorful search/magnifying glass */}
      <circle cx="270" cy="150" r="40" fill="none" stroke="#7B68EE" strokeWidth="4" opacity="0.5" />
      <path d="M300 180 L320 200" stroke="#7B68EE" strokeWidth="4" strokeLinecap="round" opacity="0.5" />
      
      {/* Colorful sparks/stars */}
      <path d="M250 80 L255 95 L270 95 L258 105 L263 120 L250 110 L237 120 L242 105 L230 95 L245 95 Z" fill="#F5A623" opacity="0.6" />
      <path d="M320 100 L322 108 L330 108 L324 113 L326 121 L320 116 L314 121 L316 113 L310 108 L318 108 Z" fill="#FF6B9D" opacity="0.6" />
    </svg>
  );
}
