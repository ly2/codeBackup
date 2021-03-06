
/*
 * Writer:
 * Version: 0.1
 * Time: 20/10/2015
 * 
 * */

/*
 * Writer:
 * Version: 0.2
 * Time: 21/10/2015
 * 
 * */

public class Premium extends Member{
	
	private double rentFeeDVD;
	private double rentFeeVCD;
	private double renewFeeDVD;
	private double renewFeeVCD;
	private double lateFee;
	private double replaceFeeDVD;
	private double replaceFeeVCD;
	private double maxDVD;
	private double maxVCD;
	
	public Premium(String contactNo, String name, String add, int memberNumber) {
		super(contactNo, name, add, memberNumber);
		
		this.rentFeeDVD = 3;
		this.rentFeeVCD = 1;
		this.renewFeeDVD = 1;
		this.renewFeeVCD = 0.5;
		this.lateFee = 10;
		this.replaceFeeDVD = 30;
		this.replaceFeeVCD = 15;
		this.maxDVD = 2;
		this.maxVCD = 4;
		
	}
	
	public double getMaxDVD() {
		return maxDVD;
	}

	public void setMaxDVD(double maxDVD) {
		this.maxDVD = maxDVD;
	}

	public double getMaxVCD() {
		return maxVCD;
	}

	public void setMaxVCD(double maxVCD) {
		this.maxVCD = maxVCD;
	}

	public double getRentFeeDVD() {
		return rentFeeDVD;
	}
	public void setRentFeeDVD(double rentFeeDVD) {
		this.rentFeeDVD = rentFeeDVD;
	}
	public double getRentFeeVCD() {
		return rentFeeVCD;
	}
	public void setRentFeeVCD(double rentFeeVCD) {
		this.rentFeeVCD = rentFeeVCD;
	}
	public double getRenewFeeDVD() {
		return renewFeeDVD;
	}
	public void setRenewFeeDVD(double renewFeeDVD) {
		this.renewFeeDVD = renewFeeDVD;
	}
	public double getRenewFeeVCD() {
		return renewFeeVCD;
	}
	public void setRenewFeeVCD(double renewFeeVCD) {
		this.renewFeeVCD = renewFeeVCD;
	}
	public double getLateFee() {
		return lateFee;
	}
	public void setLateFee(double lateFee) {
		this.lateFee = lateFee;
	}
	public double getReplaceFeeDVD() {
		return replaceFeeDVD;
	}
	public void setReplaceFeeDVD(double replaceFeeDVD) {
		this.replaceFeeDVD = replaceFeeDVD;
	}
	public double getReplaceFeeVCD() {
		return replaceFeeVCD;
	}
	public void setReplaceFeeVCD(double replaceFeeVCD) {
		this.replaceFeeVCD = replaceFeeVCD;
	}

}
