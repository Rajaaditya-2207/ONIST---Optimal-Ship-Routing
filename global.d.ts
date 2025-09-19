declare module '*.css' {
  const content: { [className: string]: string };
  export default content;
}

declare module 'components/LeafletMap' {
  import { FC } from 'react';
  export interface LeafletMapProps {
    route: [number, number][] | null;
    showWeather: boolean;
    startPort: [number, number] | null;
    endPort: [number, number] | null;
    isSelectingLocation: 'start' | 'end' | null;
    onLocationSelect: (location: [number, number]) => void;
    zoomToLocation: [number, number] | null;
  }
  const LeafletMap: FC<LeafletMapProps>;
  export default LeafletMap;
}
