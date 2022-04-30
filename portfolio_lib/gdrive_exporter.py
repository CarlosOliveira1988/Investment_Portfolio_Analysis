"""This file has a set of methods to export data to GoogleDrive spreadshee."""

import os

import pandas as pd


class GoogleDriveExporter:
    """Class used to export data to GoogleDrive spreadsheet."""

    def __init__(self):
        """Create the GoogleDriveExporter object."""
        pass

    def save(
        self,
        currentPortfolio,
        extrato_path,
        auto_save=True,
        auto_open=True,
    ):
        """Save the excel file to be used in Google Drive."""
        # Get the current portfolio
        dataframe = currentPortfolio

        # Define the columns to be displayed in the exported spreadsheet
        # This will also define the columns order, that is useful to the
        # next steps
        expected_col_list = [
            "Ticker",
            "Mercado",
            "Quantidade",
            "Preço médio+taxas",
            "Preço pago",
            "Proventos",
            "Compras totais",
            "Vendas parciais",
            "Taxas Adicionais",
            "IR",
            "Cotação",
            "Preço mercado",
            "Mercado-pago",
            "Mercado-pago(%)",
            "Líquido parcial",
            "Líquido parcial(%)",
        ]
        dataframe = dataframe[expected_col_list]

        # Define the columns in the exported spreadsheet
        ticker_col = "A"
        market_col = "B"
        quantity_col = "C"
        mean_price_col = "D"
        buy_price_col = "E"
        earning_col = "F"
        total_buy_col = "G"
        partial_sell_col = "H"
        costs_col = "I"
        IR_col = "J"
        quotation_col = "K"
        mkt_price_col = "L"
        rent_gain_price_col = "M"
        gain_price_col = "N"
        net_result_col = "O"
        net_result_perc_col = "P"
        empty_col = "Q"
        chart_col = "R"
        sum_if_col = "S"

        # Add some formulas to be used in GoogleSheets
        i = 2
        for index, row in dataframe.iterrows():
            # This function takes a long time to run.
            # Not suitable to uncomment while testing.
            dfticker = dataframe["Ticker"]
            dataframe["Cotação"] = '=googlefinance("' + dfticker + '")'

            market_price_str = "=" + quantity_col + str(i)
            market_price_str += "*" + quotation_col + str(i)
            dataframe.at[index, "Preço mercado"] = market_price_str

            gain_price_str = "=" + mkt_price_col + str(i)
            gain_price_str += "-" + buy_price_col + str(i)
            dataframe.at[index, "Mercado-pago"] = gain_price_str

            rent_gain_str = "=" + rent_gain_price_col + str(i)
            rent_gain_str += "/" + buy_price_col + str(i)
            dataframe.at[index, "Mercado-pago(%)"] = rent_gain_str

            net_result_str = "=" + mkt_price_col + str(i)
            net_result_str += "+" + partial_sell_col + str(i)
            net_result_str += "+" + earning_col + str(i)
            net_result_str += "-" + costs_col + str(i)
            net_result_str += "-" + IR_col + str(i)
            net_result_str += "-" + total_buy_col + str(i)
            dataframe.at[index, "Líquido parcial"] = net_result_str

            net_perc_str = "=" + net_result_col + str(i)
            net_perc_str += "/" + buy_price_col + str(i)
            dataframe.at[index, "Líquido parcial(%)"] = net_perc_str
            # Increment the index to calculate the cells in Excel file.
            i += 1

        if auto_save:
            # Create a Pandas Excel writer using XlsxWriter as the engine
            file_name = "carteiraGoogleDrive.xlsx"
            file = os.path.join(extrato_path, file_name)
            writer = pd.ExcelWriter(file, engine="xlsxwriter")

            # Convert the dataframe to an XlsxWriter Excel object.
            dataframe.to_excel(writer, sheet_name="Sheet1", index=False)

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            # Add some cell formats.
            formatFloat = workbook.add_format(
                {"num_format": "#,##0.00", "align": "center"},
            )
            formatText = workbook.add_format(
                {"align": "center"},
            )
            formatPerc = workbook.add_format(
                {"num_format": "0.00%", "align": "center"},
            )
            formatBorder = workbook.add_format(
                {"bottom": 1, "top": 1, "left": 1, "right": 1},
            )
            bold = workbook.add_format(
                {"bold": True, "align": "center"},
            )

            # Green fill with dark green text.
            formatGreen = workbook.add_format(
                {"bg_color": "#C6EFCE", "font_color": "#006100"},
            )

            # Light red fill with dark red text.
            formatRed = workbook.add_format(
                {"bg_color": "#FFC7CE", "font_color": "#9C0006"},
            )

            # Conditional formatting. If values are greater equal than zero
            df_len = str(len(dataframe) + 1)
            worksheet.conditional_format(
                rent_gain_price_col + "2:" + net_result_perc_col + df_len,
                {
                    "type": "cell",
                    "criteria": ">=",
                    "value": 0,
                    "format": formatGreen,
                },
            )

            # Conditional formatting.If values are lesser than zero
            worksheet.conditional_format(
                rent_gain_price_col + "2:" + net_result_perc_col + df_len,
                {
                    "type": "cell",
                    "criteria": "<",
                    "value": 0,
                    "format": formatRed,
                },
            )

            # Note: It isn't possible to format any cells that
            # already have a format such as the index or headers
            # or any cells that contain dates or datetimes.

            # Set the column width and format
            def formatAsText(col_list, width=18):
                for col in col_list:
                    worksheet.set_column(col + ":" + col, width, formatText)

            def formatAsFloat(col_list, width=18):
                for col in col_list:
                    worksheet.set_column(col + ":" + col, width, formatFloat)

            def formatAsPercentage(col_list, width=18):
                for col in col_list:
                    worksheet.set_column(col + ":" + col, width, formatPerc)

            formatAsText(
                [
                    ticker_col,
                    market_col,
                ]
            )
            formatAsFloat(
                [
                    quantity_col,
                    mean_price_col,
                    buy_price_col,
                    earning_col,
                    total_buy_col,
                    partial_sell_col,
                    costs_col,
                    IR_col,
                    quotation_col,
                    mkt_price_col,
                ]
            )
            formatAsFloat(
                [
                    rent_gain_price_col,
                    net_result_col,
                ],
                width=25,
            )
            formatAsPercentage(
                [
                    gain_price_col,
                    net_result_perc_col,
                ],
                width=25,
            )

            # Create supplementary table to support graphic of percentage
            # List of category
            formatAsText([chart_col])
            worksheet.write(chart_col + "1", "Ativo", bold)
            worksheet.write(chart_col + "2", "Ações")
            worksheet.write(chart_col + "3", "BDR")
            worksheet.write(chart_col + "4", "ETF")
            worksheet.write(chart_col + "5", "FII")

            # Create list of the values
            formatAsFloat([sum_if_col], width=20)
            start_sumif = "=SUMIF(" + market_col + "2:" + market_col + '100, "'
            endsumif = '", ' + mkt_price_col + "2:" + mkt_price_col + "100)"
            worksheet.write(sum_if_col + "1", "Valor R$", bold)
            worksheet.write(sum_if_col + "2", start_sumif + "Ações" + endsumif)
            worksheet.write(sum_if_col + "3", start_sumif + "BDR" + endsumif)
            worksheet.write(sum_if_col + "4", start_sumif + "ETF" + endsumif)
            worksheet.write(sum_if_col + "5", start_sumif + "FII" + endsumif)

            # Create conditional format for borders
            chart_table_range = chart_col + "1:" + sum_if_col + "5"
            worksheet.conditional_format(
                chart_table_range,
                {"type": "no_errors", "format": formatBorder},
            )

            # Creates a Pie chart
            chart1 = workbook.add_chart({"type": "pie"})

            # Configure the series and add user defined segment colors
            categ_range = "=Sheet1!$" + chart_col + "$2:$" + chart_col + "$5"
            val_range = "=Sheet1!$" + sum_if_col + "$2:$" + sum_if_col + "$5"
            chart1.add_series(
                {
                    "data_labels": {"percentage": True},
                    "categories": categ_range,
                    "values": val_range,
                }
            )

            # Add a title
            chart1.set_title({"name": "Composição da carteira"})

            # Insert the chart into the worksheet (with an offset)
            chart_cell = chart_col + "8"
            worksheet.insert_chart(
                chart_cell,
                chart1,
                {"x_offset": 25, "y_offset": 10},
            )

            # Close the Pandas Excel writer and output the Excel file
            writer.save()

            if auto_open:
                try:
                    os.startfile(file)
                finally:
                    pass

        return dataframe
