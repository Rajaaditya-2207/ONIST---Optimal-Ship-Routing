import React from 'react';
import { motion } from 'framer-motion';
import { Lightbulb } from 'lucide-react';

interface ExplanationProps {
  explanation: string;
  isNavOpen: boolean;
}

const Explanation: React.FC<ExplanationProps> = ({ explanation, isNavOpen }) => {
  if (!explanation) {
    return null;
  }

  return (
    <motion.div 
      className="mt-8 p-4 border-l-4 border-emerald-500 bg-emerald-50 dark:bg-gray-700 rounded-r-lg"
      animate={{ opacity: isNavOpen ? 1 : 0 }}
      initial={{ opacity: 0 }}
    >
      <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 flex items-center mb-2">
        <Lightbulb className="mr-2 text-emerald-500" /> Route Explanation
      </h3>
      <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
        {explanation}
      </p>
    </motion.div>
  );
};

export default Explanation;
