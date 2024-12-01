export interface BirthChartFormData {
    birth_date: string;
    birth_time: string;
    birth_location: string;
    house_system: string;
  }
  
  export interface BirthChartData {
    sun_sign: string;
    moon_sign: string;
    ascendant_sign: string;
    planetary_positions: {
      [key: string]: string;
    };
    birth_chart: {
      houses: {
        [key: string]: string;
      };
    };
  }
  
  