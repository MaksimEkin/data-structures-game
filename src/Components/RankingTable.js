import React, { useMemo } from 'react'
import { useTable } from 'react-table'
import MOCK_DATA from './MOCK_LEADERBOARD_DATA.json'
import { COLUMNS } from './Columns'

export const RankingTable = () => {
	
	const columns = useMemo(() => COLUMNS, [])
	const data = useMemo(() => MOCK_DATA, [])
	
	const tableInstance = useTable({
		columns,
		data
	})
	
	const { 
		getTableProps, 
		getTableBodyProps, 
		headerGroups, 
		rows, 
		prepareRow,
	} = tableInstance
	
	return (
		<table {...getTableProps()}>
			<thead>
				{
					headerGroups.map((headerGroup) => (
				}
				<tr {...headerGroup.getHeaderGroupProps()}>
					{
						headerGroup.headers.map( column =>
					}
					<th></th>
				</tr>
			</thead>
			<tbody {...getTableBodyProps()}>
				<tr>
					<td></td>
				</tr>
			</tbody>
		</table>
	)
}
