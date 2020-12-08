import React, { useMemo } from 'react'
import { useTable, useSortBy } from 'react-table'
import { COLUMNS } from './Columns'

export const RankingTable = ({data}) => {

	const columns = useMemo(() => COLUMNS, []) /* get columns from columns file */

	const {  // set up table instance
		getTableProps,
		getTableBodyProps,
		headerGroups,
		footerGroups, 
		rows,
		prepareRow,
	} = useTable({  // define initial sort of data (highest score first on default)
		columns,
		data,
		initialState: {
		  sortBy: [{ id: 'points', desc: true }]
		}
	},
	useSortBy)

	return (<div>
		<link href="https://unpkg.com/tailwindcss@0.3.0/dist/tailwind.min.css" rel="stylesheet"></link> {/* link to stylesheet for profile */}
		<table className="text-left w-full border-collapse bg-white shadow-2xl rounded my-6" {...getTableProps()}>
			<thead>
				{headerGroups.map((headerGroup) => ( /* render the header */
					<tr {...headerGroup.getHeaderGroupProps()}>
						{headerGroup.headers.map((column) => (
							<th className="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light" {...column.getHeaderProps(column.getSortByToggleProps())}> 
							  {column.render('Header')}
							  <span /* allow user to sort ranking table*/> 
								  {column.isSorted ? (column.isSortedDesc ? ' ⬇️' : ' ⬆️') : ''} 
							  </span>
							</th>
						))}
					</tr>
				))}
			</thead>
			<tbody {...getTableBodyProps()}>
				{rows.map((row) => {
					prepareRow(row)
					return (
						<tr {...row.getRowProps()}>
							{row.cells.map((cell) => { /* display table data */
								return <td className="py-4 px-6 border-b border-grey-light" {...cell.getCellProps()}>{cell.render('Cell')}</td>
							})}
						</tr>
					)
				})}
			</tbody>
		</table>
	</div>)
}
