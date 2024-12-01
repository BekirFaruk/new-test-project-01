// astro-frontend/components/BirthChartForm.tsx
import { useForm, SubmitHandler } from 'react-hook-form';
import axios from 'axios';
import { BirthChartFormData, BirthChartData } from '../types/birthChart';

interface BirthChartFormProps {
  onSubmit: (data: BirthChartData) => void;
}

const houseSystems = ['Placidus', 'Koch', 'Whole Sign', 'Equal', 'Campanus', 'Regiomontanus', 'Porphyrius'];

export default function BirthChartForm({ onSubmit }: BirthChartFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<BirthChartFormData>();

  const onSubmitForm: SubmitHandler<BirthChartFormData> = async (data) => {
    try {
      const response = await axios.post('http://localhost:5000/calculate_birth_chart', data);
      onSubmit(response.data);
    } catch (error) {
      console.error('Error fetching birth chart data:', error);
      alert('An error occurred while fetching the birth chart data. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-4">
      <div>
        <label htmlFor="birthDate" className="block text-sm font-medium text-gray-700">Birth Date</label>
        <input
          type="date"
          id="birthDate"
          {...register('birth_date', { required: 'Birth date is required' })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
        {errors.birth_date && <p className="mt-1 text-sm text-red-600">{errors.birth_date.message}</p>}
      </div>

      <div>
        <label htmlFor="birthTime" className="block text-sm font-medium text-gray-700">Birth Time</label>
        <input
          type="time"
          id="birthTime"
          {...register('birth_time', { required: 'Birth time is required' })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
        {errors.birth_time && <p className="mt-1 text-sm text-red-600">{errors.birth_time.message}</p>}
      </div>

      <div>
        <label htmlFor="birthLocation" className="block text-sm font-medium text-gray-700">Birth Location</label>
        <input
          type="text"
          id="birthLocation"
          {...register('birth_location', { required: 'Birth location is required' })}
          placeholder="City, Country"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
        {errors.birth_location && <p className="mt-1 text-sm text-red-600">{errors.birth_location.message}</p>}
      </div>

      <div>
        <label htmlFor="houseSystem" className="block text-sm font-medium text-gray-700">House System</label>
        <select
          id="houseSystem"
          {...register('house_system', { required: 'House system is required' })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        >
          {houseSystems.map((system) => (
            <option key={system} value={system}>{system}</option>
          ))}
        </select>
        {errors.house_system && <p className="mt-1 text-sm text-red-600">{errors.house_system.message}</p>}
      </div>

      <button
        type="submit"
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Calculate Birth Chart
      </button>
    </form>
  );
}