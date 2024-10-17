import React, { useState } from 'react';

interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number;
  type: 'income' | 'expense';
}

const Transactions: React.FC = () => {
  const [transactions] = useState<Transaction[]>([
    { id: 1, date: '2024-10-15', description: 'Salary', amount: 3000, type: 'income' },
    { id: 2, date: '2024-10-16', description: 'Grocery shopping', amount: 150, type: 'expense' },
    { id: 3, date: '2024-10-17', description: 'Freelance work', amount: 500, type: 'income' },
  ]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-100">Transactions</h2>
      <div className="bg-gray-800 shadow-md rounded overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left text-gray-300">Date</th>
              <th className="p-3 text-left text-gray-300">Description</th>
              <th className="p-3 text-right text-gray-300">Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id} className="border-b border-gray-700">
                <td className="p-3 text-gray-300">{transaction.date}</td>
                <td className="p-3 text-gray-300">{transaction.description}</td>
                <td className={`p-3 text-right ${transaction.type === 'income' ? 'text-green-400' : 'text-red-400'}`}>
                  {transaction.type === 'income' ? '+' : '-'}${transaction.amount.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Transactions;