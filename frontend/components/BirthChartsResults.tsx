import { BirthChartData } from '../types/birthChart';

interface BirthChartResultsProps {
  data: BirthChartData;
  onReset: () => void;
}

import React from 'react';

export default function BirthChartResults({ data, onReset }: BirthChartResultsProps) {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-900">Birth Chart Results</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-semibold text-lg mb-2">Sun Sign</h3>
          <p>{data.sun_sign}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-semibold text-lg mb-2">Moon Sign</h3>
          <p>{data.moon_sign}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-semibold text-lg mb-2">Ascendant Sign</h3>
          <p>{data.ascendant_sign}</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold text-lg mb-2">Planetary Positions</h3>
        <ul className="list-disc list-inside">
          {Object.entries(data.planetary_positions).map(([planet, position]) => (
            <li key={planet}>{planet}: {position}</li>
          ))}
        </ul>
      </div>

      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold text-lg mb-2">Birth Chart</h3>
        <ul className="list-disc list-inside">
          {Object.entries(data.birth_chart.houses).map(([house, sign]) => (
            <li key={house}>{house}: {sign}</li>
          ))}
        </ul>
      </div>

      <button
        onClick={onReset}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Calculate Another Chart
      </button>
    </div>
  );
}

