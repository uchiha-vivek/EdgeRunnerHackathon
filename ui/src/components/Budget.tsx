import React, { useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';

interface BudgetCategory {
  name: string;
  amount: number;
}

const COLORS = ['#60A5FA', '#34D399', '#FBBF24', '#F87171', '#A78BFA'];

const Budget: React.FC = () => {
  const [categories, setCategories] = useState<BudgetCategory[]>([
    { name: 'Housing', amount: 1000 },
    { name: 'Food', amount: 500 },
    { name: 'Transportation', amount: 300 },
    { name: 'Entertainment', amount: 200 },
    { name: 'Savings', amount: 400 },
  ]);

  const totalBudget = categories.reduce((sum, category) => sum + category.amount, 0);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-100">Budget Overview</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-4 text-gray-300">Budget Breakdown</h3>
          <ul className="space-y-2">
            {categories.map((category, index) => (
              <li key={index} className="flex justify-between items-center py-2 border-b border-gray-700 last:border-b-0">
                <span className="text-gray-300">{category.name}</span>
                <span className="font-semibold text-gray-100">${category.amount}</span>
              </li>
            ))}
          </ul>
          <p className="mt-4 text-right font-bold text-gray-100">Total: ${totalBudget}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-4 text-gray-300">Budget Distribution</h3>
          <div className="h-64 sm:h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categories}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius="80%"
                  fill="#8884d8"
                  dataKey="amount"
                >
                  {categories.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Budget;