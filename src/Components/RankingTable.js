import React, { useMemo } from 'react'
import { useTable, useSortBy } from 'react-table'
import MOCK_DATA from './MOCK_LEADERBOARD_DATA.json'
import { COLUMNS } from './Columns'

export const RankingTable = () => {

	const columns = useMemo(() => COLUMNS, [])
	const data = useMemo(() => MOCK_DATA, [])

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
		  sortBy: [{ id: 'total_score', desc: true }]
		}
	},
	useSortBy)

	return (
		<table {...getTableProps()}>
			<thead>
				{headerGroups.map((headerGroup) => ( /* render the header */
					<tr {...headerGroup.getHeaderGroupProps()}>
						{headerGroup.headers.map((column) => (
							<th {...column.getHeaderProps(column.getSortByToggleProps())}> 
							  {column.render('Header')}
							  <span /* make sorting */> 
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
							{row.cells.map((cell) => {
								return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
							})}
						</tr>
					)
				})}
			</tbody>
			<tfoot>
				{footerGroups.map(footerGroup => (
					<tr {...footerGroup.getFooterGroupProps()}>
						{footerGroup.headers.map((column) => (
							<td {...column.getFooterProps}> {column.render('Footer')}</td>
						))}
					</tr>
				))}
			</tfoot>
		</table>
	)
}
