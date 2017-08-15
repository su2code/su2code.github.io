//outputs a mailto link in the form:
//<a href="mailto:[addr]@[domain]">[addr]@[domain]</a>
function printEmail(addr, domain)
{
	//var domain = 'stanford.edu';
	document.write('<a href=\"mailto:' + addr + '@' + domain + '\">');
	document.write(addr + "@" + domain + '</a>');
}