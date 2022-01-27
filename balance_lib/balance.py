"""This file is useful to handle portfolio balancing."""

import numpy as np
import pandas as pd


class InvestmentBox:
    """Class used to handle investment boxes."""

    def __init__(self, box_title, auto_total_line=True):
        """Create the InvestmentBox object.

        Arguments:
        - box_title: a string for the box title
        """
        self.box_title = box_title
        self.auto_total_line = auto_total_line
        self.__createDataframe()
        self.__setTotalLine()

    """Private methods."""

    def __checkLists(self, target_list, value_list, type_list):
        # Look for some failure conditions
        target_len = len(target_list)
        value_len = len(value_list)
        type_len = len(type_list)
        sum_len = target_len + value_len + type_len
        if target_len == 0:
            msg = "The 'target_list' length is zero."
            raise ValueError(msg)
        elif value_len == 0:
            msg = "The 'value_list' length is zero."
            raise ValueError(msg)
        elif type_len == 0:
            msg = "The 'type_list' length is zero."
            raise ValueError(msg)
        elif (3 * target_len) != sum_len:
            msg = "All lists must have the same length."
            raise ValueError(msg)

    def __createDataframe(self):
        # Create the box dataframe with some specific columns
        col_list = [
            self.box_title,
            "Meta(%)",
            "Meta(R$)",
            "Atual(%)",
            "Atual(R$)",
        ]
        self.df = pd.DataFrame(columns=col_list)
        self.current_total = self.df["Atual(R$)"].sum()

    def __appendData(self, target_list, value_list, type_list):
        # Insert the lists in the dataframe
        data_dict = {
            self.box_title: type_list,
            "Meta(%)": target_list,
            "Meta(R$)": [0] * len(target_list),
            "Atual(%)": [0] * len(target_list),
            "Atual(R$)": value_list,
        }
        df = pd.DataFrame(data=data_dict)
        self.df = pd.concat([self.df, df], ignore_index=True, sort=False)
        self.current_total = self.df["Atual(R$)"].sum()

    def __calculateDFRelatedValues(self):
        # Calculate the columns
        self.df["Meta(R$)"] = self.df["Meta(%)"] * self.current_total
        self.df["Atual(%)"] = self.df["Atual(R$)"] / self.current_total

    def __setTotalLine(self):
        # Create the total line
        data_dict = {
            self.box_title: "TOTAL",
            "Meta(%)": self.df["Meta(%)"].sum(),
            "Meta(R$)": self.df["Meta(R$)"].sum(),
            "Atual(%)": self.df["Atual(%)"].sum(),
            "Atual(R$)": self.df["Atual(R$)"].sum(),
        }
        if self.auto_total_line:
            self.df = self.df.append(data_dict, ignore_index=True)

    """Public methods."""

    def setValues(self, target_list, value_list, type_list):
        """Set the target percentage according to the investment type.

        Arguments:
        - type_list: a list of strings related to investment types
        - value_list: a list of values (the money)
        - target_list: a list of percentage targets per investment type

        The 'type_list' and 'target_list' must have the same length.
        """
        self.__checkLists(target_list, value_list, type_list)
        self.__createDataframe()
        self.__appendData(target_list, value_list, type_list)
        self.__calculateDFRelatedValues()
        self.__setTotalLine()

    def getTotalValue(self):
        """Return the sum of the current values."""
        return self.current_total

    def getDataframe(self):
        """Return the InvestmentBox dataframe.

        The following columns are present:
        - 1st column title: defined by the 'box_title' parameter
        - 2nd column: 'Meta(%)'
        - 3rd column: 'Meta(R$)'
        - 4th column: 'Atual(%)'
        - 5th column: 'Atual(R$)'
        """
        return self.df.copy()


class ContributionBox:
    """Class used to handle financial contributions."""

    def __init__(self, box_title):
        """Create the ContributionBox object.

        Arguments:
        - box_title: a string for the box title
        """
        self.box_title = box_title
        self.ibox = InvestmentBox(box_title, auto_total_line=False)
        self.contribution = 0.0
        self.total_plus_contribution = 0.0
        self.filter_contribution_sum = 0.0
        self.expected_output_columns = [
            box_title,
            "Meta(%)",
            "Meta(R$)",
            "Atual(%)",
            "Atual(R$)",
            "Desejado",
            "Desejado-Atual",
            "Aporte Real",
        ]
        self.__calculateTotalPlusContribution()
        self.__calculateDFRelatedValues()
        self.__setTotalLine()

    """Private methods."""

    def __calculateTotalPlusContribution(self):
        total = self.ibox.getTotalValue() + self.contribution
        self.total_plus_contribution = total

    def __calculateDFRelatedValues(self):
        self.df = self.ibox.getDataframe()
        value = self.total_plus_contribution
        self.df["Desejado"] = self.df["Meta(%)"] * value
        self.df["Desejado-Atual"] = self.df["Desejado"] - self.df["Atual(R$)"]
        self.df["Filtro Aporte"] = np.where(
            self.df["Desejado-Atual"] > 0.0, self.df["Desejado-Atual"], 0.0
        )
        self.filter_contribution_sum = self.df["Filtro Aporte"].sum()
        try:
            proportion = self.contribution / self.filter_contribution_sum
        except ZeroDivisionError:
            proportion = 0.0
        self.df["Aporte Real"] = self.df["Filtro Aporte"] * proportion

    def __setTotalLine(self):
        data_dict = {
            self.box_title: "TOTAL",
            "Meta(%)": self.df["Meta(%)"].sum(),
            "Meta(R$)": self.df["Meta(R$)"].sum(),
            "Atual(%)": self.df["Atual(%)"].sum(),
            "Atual(R$)": self.df["Atual(R$)"].sum(),
            "Desejado": self.df["Desejado"].sum(),
            "Desejado-Atual": self.df["Desejado-Atual"].sum(),
            "Filtro Aporte": self.df["Filtro Aporte"].sum(),
            "Aporte Real": self.df["Aporte Real"].sum(),
        }
        self.df = self.df.append(data_dict, ignore_index=True)

    """Public methods."""

    def setValues(self, target_list, value_list, type_list):
        """Set the target percentage according to the investment type.

        Arguments:
        - type_list: a list of strings related to investment types
        - value_list: a list of values (the money)
        - target_list: a list of percentage targets per investment type

        The 'type_list' and 'target_list' must have the same length.
        """
        self.ibox.setValues(target_list, value_list, type_list)
        self.__calculateTotalPlusContribution()
        self.__calculateDFRelatedValues()
        self.__setTotalLine()

    def setContribution(self, value):
        """Set the financial contribution value."""
        self.contribution = value
        self.__calculateTotalPlusContribution()
        self.__calculateDFRelatedValues()
        self.__setTotalLine()

    def getContribution(self):
        """Return the financial contribution value."""
        return self.contribution

    def getTotalPlusContribution(self):
        """Return the sum of the current values with the contribution."""
        return self.total_plus_contribution

    def getDataframe(self):
        """Return the ContributionBox dataframe.

        The following columns are present:
        - 1st column title: defined by the 'box_title' parameter
        - 2nd column: 'Meta(%)'
        - 3rd column: 'Meta(R$)'
        - 4th column: 'Atual(%)'
        - 5th column: 'Atual(R$)'
        - 6th column: 'Desejado'
        - 7th column: 'Desejado-Atual'
        - 8th column: 'Aporte Real'
        """
        return self.df[self.expected_output_columns].copy()


if __name__ == "__main__":

    # Box parameters
    box_title = "Classe de investimento"
    type_list = ["Renda Variável", "Renda Fixa", "Tesouro Direto"]
    value_list = [10000, 16000, 100000]
    target_list = [0.08, 0.12, 0.80]

    # InvestmentBox
    print("\nEmpty InvestmentBox")
    ibox = InvestmentBox(box_title)
    print(ibox.getDataframe())
    print("\nFilled in InvestmentBox")
    ibox.setValues(target_list, value_list, type_list)
    print(ibox.getDataframe())

    # ContributionBox
    print("\nContributionBox")
    cbox = ContributionBox(box_title)
    cbox.setValues(target_list, value_list, type_list)
    cbox.setContribution(2000.0)
    print(cbox.getDataframe())
