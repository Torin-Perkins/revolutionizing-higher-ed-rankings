// Embed CSV data directly into the JS
const csvData = 
`Index,University,Artificial Intelligence,Machine Learning,Cybersecurity,Bioinformatics,Computer Systems and Networks,Databases and Data Mining,Human Computer Interaction,Vision and Graphics
1,Arizona State University,1000,669,874,800,836,926,977,601
2,Georgia State University,950,990,970,636,828,889,886,984
3,Stanford University,900,618,870,775,635,686,860,885
4,Purdue University,880,735,628,744,600,893,739,712
5,Johns Hopkins University,875,860,650,670,882,986,851,729
6,Duke University,860,691,680,859,879,979,710,790
7,Oregon State University,855,996,823,603,603,834,660,797
8,California Institute of Technology,830,886,619,911,788,936,884,714
9,Elon University,820,701,753,792,954,648,942,887
10,New York University,805,926,644,954,961,806,960,705
11,Drexel University,795,784,646,702,970,680,954,751
12,Boston University,785,744,870,693,776,736,928,656
13,University of Florida,770,727,896,765,760,729,956,621
14,Virginia Tech,755,822,880,813,734,919,989,770
15,Rice University,740,963,709,851,608,970,1000,679
16,Baylor University,725,688,827,975,722,745,740,782
17,University of Denver,710,785,877,890,940,963,773,760
18,Vanderbilt University,695,869,736,645,791,908,895,822
19,University of Georgia,680,918,899,743,889,900,900,683
20,Princeton University,665,918,782,980,896,992,894,838
`;

// Process CSV data
const rows = csvData.trim().split('\n');
const headers = rows.shift().split(',');
const data = rows.map(row => {
	const rowData = row.split(',');
	return headers.reduce((obj, header, index) => {
		obj[header.trim()] = rowData[index].trim();
		return obj;
	}, {});
});

console.log(data);

function getScore(universityName, categoryName) {
    // Find the row corresponding to the university
    const row = data.find(entry => entry.University === universityName);
    
    if (!row) {
        console.log(`University '${universityName}' not found.`);
        return null;
    }

    // Return the score for the given category
    const score = row[categoryName];
    
    if (score === undefined) {
        console.log(`Category '${categoryName}' not found.`);
        return null;
    }

    return parseInt(score); // Parse score as integer
}

// Example usage
const universityName = "Stanford University";
const categoryName = "Artificial Intelligence";
const score = getScore(universityName, categoryName);

if (score !== null) {
    console.log(`Score for ${categoryName} at ${universityName}: ${score}`);
}
