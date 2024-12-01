import { useState } from 'react';
import Head from 'next/head';
import BirthChartForm from '../components/BirthChartForm';
// Removed BirthChartResults import due to the error
import { BirthChartData } from '../types/birthChart';
import React from 'react';
import BirthChartResults from '../components/BirthChartsResults';

export default function Home() {
  const [birthChartData, setBirthChartData] = useState<BirthChartData | null>(null);

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <Head>
        <title>Astrology Birth Chart Calculator</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <h1 className="text-4xl font-bold text-center mb-8 text-gray-900">Astrology Birth Chart Calculator</h1>
          {!birthChartData ? (
            <BirthChartForm onSubmit={setBirthChartData} />
          ) : (
            <BirthChartResults data={birthChartData} onReset={() => setBirthChartData(null)} />
          )}
        </div>
      </main>
    </div>
  );
}