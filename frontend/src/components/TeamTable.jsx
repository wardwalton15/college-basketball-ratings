import React, { useState, useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
} from '@tanstack/react-table';
import TeamDetail from './TeamDetail';
import './TeamTable.css';

function TeamTable({ teams }) {
  const [sorting, setSorting] = useState([{ id: 'overall_rating', desc: true }]);
  const [expandedRow, setExpandedRow] = useState(null);

  // Define columns
  const columns = useMemo(
    () => [
      {
        accessorKey: 'overall_rank',
        header: 'Rank',
        cell: (info) => info.getValue(),
        size: 60,
      },
      {
        accessorKey: 'team_name',
        header: 'Team',
        cell: (info) => (
          <div className="team-name">
            <strong>{info.getValue()}</strong>
            {info.row.original.conference && (
              <span className="conference">{info.row.original.conference}</span>
            )}
          </div>
        ),
        size: 200,
      },
      {
        accessorKey: 'overall_rating',
        header: 'Rating',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
      {
        accessorKey: 'offensive_rating',
        header: 'OFF',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
      {
        accessorKey: 'defensive_rating',
        header: 'DEF',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
      {
        accessorKey: 'off_efg',
        header: 'eFG%',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
      {
        accessorKey: 'off_orb',
        header: 'ORB%',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
      {
        accessorKey: 'off_tov',
        header: 'TOV%',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
      {
        accessorKey: 'off_ftr',
        header: 'FTR',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
      {
        accessorKey: 'tempo',
        header: 'Tempo',
        cell: (info) => info.getValue()?.toFixed(1) || 'N/A',
        size: 80,
      },
    ],
    []
  );

  const table = useReactTable({
    data: teams,
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  const handleRowClick = (rowId) => {
    setExpandedRow(expandedRow === rowId ? null : rowId);
  };

  if (teams.length === 0) {
    return null;
  }

  return (
    <div className="team-table-container">
      <div className="table-scroll">
        <table className="team-table">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    style={{ width: header.column.columnDef.size }}
                    className={header.column.getCanSort() ? 'sortable' : ''}
                    onClick={header.column.getToggleSortingHandler()}
                  >
                    <div className="header-content">
                      {flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                      {header.column.getIsSorted() && (
                        <span className="sort-indicator">
                          {header.column.getIsSorted() === 'desc' ? ' ↓' : ' ↑'}
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <React.Fragment key={row.id}>
                <tr
                  className={`team-row ${expandedRow === row.id ? 'expanded' : ''}`}
                  onClick={() => handleRowClick(row.id)}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
                {expandedRow === row.id && (
                  <tr className="detail-row">
                    <td colSpan={columns.length}>
                      <TeamDetail team={row.original} />
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>

      <div className="table-info">
        <p>
          Showing {table.getRowModel().rows.length} teams • Click any row to view details
        </p>
      </div>
    </div>
  );
}

export default TeamTable;
